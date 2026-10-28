"""Read-only format probes on raw NSD / NSD-Imagery inputs (T-005)."""

from __future__ import annotations

import itertools
import json
from pathlib import Path
from typing import Any

import h5py
import nibabel as nib
import numpy as np
from scipy.io import loadmat

from mirage_ablation.config.paths import (
    imagery_beta_h5,
    nsdgeneral_roi,
    perception_beta_session_h5,
    perception_beta_session_nii,
    raw_nsd_dir,
    raw_nsd_imagery_dir,
)


def _h5_dataset_info(path: Path) -> dict[str, Any]:
    info: dict[str, Any] = {"path": str(path), "datasets": {}}
    with h5py.File(path, "r") as f:
        def visit(name: str, obj: h5py.Dataset | h5py.Group) -> None:
            if isinstance(obj, h5py.Dataset):
                info["datasets"][name] = {
                    "shape": obj.shape,
                    "dtype": str(obj.dtype),
                    "chunks": obj.chunks,
                }

        f.visititems(visit)
    return info


def _nifti_info(path: Path) -> dict[str, Any]:
    img = nib.load(path)
    data = np.asanyarray(img.dataobj)
    uniq = np.unique(data[np.isfinite(data)])
    return {
        "path": str(path),
        "shape": data.shape,
        "dtype": str(data.dtype),
        "unique_values_sample": uniq[:20].tolist(),
        "unique_count": int(len(uniq)),
    }


def _mask_unique_values(path: Path) -> list[float]:
    img = nib.load(path)
    data = np.asanyarray(img.dataobj)
    return sorted({float(x) for x in np.unique(data) if np.isfinite(x)})


def _infer_voxel_order(
    nii_path: Path,
    h5_path: Path,
    *,
    n_trials: int = 10,
) -> dict[str, Any]:
    """Find axis permutation where HDF5 masked vectors match NIfTI dataobj slices."""
    img = nib.load(nii_path)
    spatial_shape = img.shape[:3]
    with h5py.File(h5_path, "r") as f:
        betas = f["betas"]
        if betas.ndim != 4:
            raise ValueError(f"expected 4D betas dataset, got shape {betas.shape}")
        h5_shape = betas.shape

    permutations = list(itertools.permutations(range(3)))
    results: dict[str, Any] = {"spatial_shape": spatial_shape, "h5_shape": h5_shape}

    with h5py.File(h5_path, "r") as f:
        betas = f["betas"]
        for perm in permutations:
            perm_list = list(perm)
            ok = True
            for t in range(
                min(n_trials, betas.shape[0], img.shape[3] if img.ndim == 4 else 1)
            ):
                nii_slice = np.asanyarray(
                    img.dataobj[..., t] if img.ndim == 4 else img.dataobj
                )
                h5_slice = np.array(betas[t], dtype=np.float32)
                if np.issubdtype(betas.dtype, np.integer):
                    h5_slice = h5_slice / 300.0
                h5_reordered = np.transpose(h5_slice, perm_list)
                if h5_reordered.shape != nii_slice.shape or not np.array_equal(
                    h5_reordered, nii_slice, equal_nan=True
                ):
                    ok = False
                    break
            if ok:
                results["voxel_order"] = perm_list
                results["match_trials"] = min(
                    n_trials, betas.shape[0], img.shape[3] if img.ndim == 4 else 1
                )
                return results

    results["voxel_order"] = None
    results["error"] = "no permutation matched NIfTI for probe trials"
    return results


def _read_mat_structure(path: Path) -> dict[str, Any]:
    out: dict[str, Any] = {"path": str(path), "reader": None, "keys": []}
    try:
        data = loadmat(path, simplify_cells=True)
        out["reader"] = "scipy"
        out["keys"] = [k for k in data if not k.startswith("__")]
        return out
    except NotImplementedError:
        pass
    with h5py.File(path, "r") as f:
        out["reader"] = "h5py"
        out["keys"] = list(f.keys())
    return out


def _design_trial_count(design_dir: Path) -> int | None:
    dm = design_dir / "designmatrixGLMsingle.mat"
    if not dm.is_file():
        return None
    try:
        data = loadmat(dm, simplify_cells=True)
    except NotImplementedError:
        with h5py.File(dm, "r") as f:
            for key in f.keys():
                obj = f[key]
                if hasattr(obj, "shape") and len(obj.shape) >= 2:
                    return int(obj.shape[1])
        return None
    for key, val in data.items():
        if key.startswith("__"):
            continue
        arr = np.asarray(val)
        if arr.ndim >= 2:
            return int(arr.shape[1])
    return None


def run_format_probe(subject: int, beta_version: str) -> dict[str, Any]:
    """Collect format metadata for one subject (read-only)."""
    design_dir = raw_nsd_imagery_dir() / "experiments" / "nsdimagery"
    h5_sess = perception_beta_session_h5(subject, 1, beta_version)
    h5_img = imagery_beta_h5(subject, beta_version)
    nii_sess = perception_beta_session_nii(subject, 1, beta_version)
    roi = nsdgeneral_roi(subject)
    responses = (
        raw_nsd_dir() / "ppdata" / f"subj{subject:02d}" / "behav" / "responses.tsv"
    )

    report: dict[str, Any] = {
        "subject": subject,
        "beta_version": beta_version,
        "perception_session_h5": _h5_dataset_info(h5_sess) if h5_sess.is_file() else {"missing": str(h5_sess)},
        "imagery_h5": _h5_dataset_info(h5_img) if h5_img.is_file() else {"missing": str(h5_img)},
        "perception_session_nii": _nifti_info(nii_sess) if nii_sess.is_file() else {"missing": str(nii_sess)},
        "nsdgeneral": _nifti_info(roi) if roi.is_file() else {"missing": str(roi)},
        "nsdgeneral_unique_values": _mask_unique_values(roi) if roi.is_file() else [],
    }

    if h5_sess.is_file() and nii_sess.is_file():
        report["axis_probe"] = _infer_voxel_order(nii_sess, h5_sess)

    mat_names = [
        raw_nsd_dir() / "experiments" / "nsd" / "nsd_expdesign.mat",
        design_dir / "designmatrixGLMsingle.mat",
        design_dir / "A_pair_list.mat",
        design_dir / "B_pair_list.mat",
        design_dir / "C_pair_list.mat",
    ]
    for label in ("visA_dm", "visB_dm", "visC_dm", "imgA_1_dm", "attA_dm"):
        mat_names.append(design_dir / f"{label}.mat")

    report["mat_files"] = [
        _read_mat_structure(p) if p.is_file() else {"path": str(p), "missing": True}
        for p in mat_names
    ]

    if responses.is_file():
        lines = responses.read_text().strip().splitlines()
        report["responses_tsv_rows"] = max(0, len(lines) - 1)
    else:
        report["responses_tsv_rows"] = None
        report["responses_missing"] = str(responses)

    if h5_img.is_file():
        with h5py.File(h5_img, "r") as f:
            ds = f["betas"]
            report["imagery_beta_trials"] = int(ds.shape[0])
    else:
        report["imagery_beta_trials"] = None

    design_trials = _design_trial_count(design_dir)
    report["design_matrix_trials"] = design_trials
    report["imagery_trial_count_match"] = (
        report.get("imagery_beta_trials") == design_trials
        if design_trials is not None and report.get("imagery_beta_trials") is not None
        else None
    )

    return report


def validate_probe_report(report: dict[str, Any]) -> list[str]:
    """Return human-readable failures against T-005 acceptance criteria."""
    failures: list[str] = []
    axis = report.get("axis_probe") or {}
    if not axis.get("voxel_order"):
        failures.append("axis permutation probe failed (no exact match for 10 trials)")
    uniq = report.get("nsdgeneral_unique_values") or []
    if 1.0 not in uniq and 1 not in uniq:
        failures.append("nsdgeneral unique values do not include 1")
    if report.get("imagery_trial_count_match") is not True:
        failures.append(
            f"imagery betas trial count {report.get('imagery_beta_trials')} "
            f"!= design {report.get('design_matrix_trials')}"
        )
    for mat in report.get("mat_files", []):
        if mat.get("missing"):
            continue
        if not mat.get("reader"):
            failures.append(f"mat reader unknown for {mat.get('path')}")
    return failures


def write_probe_json(report: dict[str, Any], out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(report, indent=2))
