"""End-to-end S1 CLI tests on synthetic fixtures (T-013)."""

from __future__ import annotations

import hashlib
import shutil
from pathlib import Path

import h5py
import nibabel as nib
import numpy as np
import pytest
import yaml
from scipy.io import savemat

from mirage_ablation.config.paths import manifests_dir, smoke_root
from mirage_ablation.config.schema import NsdImageryTestManifest
from mirage_ablation.ingest.cli import main
from mirage_ablation.ingest.imagery_design import RUN_BLOCK_SPECS, design_trial_count
from mirage_ablation.ingest.s1_run import resolve_s1_paths


def _valid_manifest() -> NsdImageryTestManifest:
    path = manifests_dir() / "nsd_imagery_test_manifest_v1.json"
    if not path.is_file():
        pytest.skip("manifest not in repo")
    return NsdImageryTestManifest.model_validate_json(path.read_text())


def _cues_for_block(manifest: NsdImageryTestManifest, stim_set: str) -> list[str]:
    type_map = {"A": "simple", "B": "complex", "C": "conceptual"}
    stype = type_map[stim_set]
    return [s.letter_cue for s in manifest.imagery_stimuli if s.type == stype]


def _write_dm(path: Path, rows: int, cues: list[str]) -> None:
    savemat(
        path,
        {
            "dm": np.ones((rows, len(cues)), dtype=np.float64),
            "condit_list": np.array(cues, dtype=object),
        },
    )


@pytest.fixture
def s1_layout(repo_layout, tmp_path, synthetic_nsdgeneral_nii, synthetic_volume):
    root = repo_layout
    data = root / "data"
    nsd = data / "raw" / "nsd"
    imagery = data / "raw" / "nsd_imagery"
    design_dir = imagery / "experiments" / "nsdimagery"
    design_dir.mkdir(parents=True)
    roi = nsd / "ppdata" / "subj01" / "func1pt8mm" / "roi"
    roi.mkdir(parents=True)
    shutil.copy(synthetic_nsdgeneral_nii, roi / "nsdgeneral.nii.gz")

    manifest_src = Path(__file__).resolve().parents[2] / "manifests"
    for name in (
        "nsd_imagery_test_manifest_v1.json",
        "stimulus_overlap_audit.json",
    ):
        shutil.copy(manifest_src / name, root / "manifests" / name)
        digest = hashlib.sha256((root / "manifests" / name).read_bytes()).hexdigest()
        (root / "manifests" / f"{name}.sha256").write_text(f"{digest}  {name}\n")

    reg = yaml.safe_load((Path(__file__).resolve().parents[2] / "runs" / "registry.yaml").read_text())
    reg["provenance"]["manifest_sha256"] = hashlib.sha256(
        (root / "manifests" / "nsd_imagery_test_manifest_v1.json").read_bytes()
    ).hexdigest()
    reg["provenance"]["audit_sha256"] = hashlib.sha256(
        (root / "manifests" / "stimulus_overlap_audit.json").read_bytes()
    ).hexdigest()
    (root / "runs" / "registry.yaml").write_text(yaml.dump(reg))

    stim = nsd / "experiments" / "nsd" / "nsd_stim_info_merged.csv"
    stim.parent.mkdir(parents=True, exist_ok=True)
    stim.write_text(
        "cocoId,nsdId,shared1000,subject1,subject1_rep0,subject1_rep1,subject1_rep2\n"
        "1001,10,False,1,1,0,0\n"
    )
    behav = nsd / "ppdata" / "subj01" / "behav"
    behav.mkdir(parents=True)
    savemat(
        nsd / "experiments" / "nsd" / "nsd_expdesign.mat",
        {
            "masterordering": np.array([[1]], dtype=np.float64),
            "subjectim": np.full((8, 1), 11.0),
        },
    )
    (behav / "responses.tsv").write_text(
        "SUBJECT\tSESSION\tRUN\tTRIAL\t73KID\t10KID\n" "1\t1\t1\t1\t11\t1\n"
    )

    manifest = _valid_manifest()

    for run_label, run_type, stim_set in RUN_BLOCK_SPECS:
        rows = 60 if run_type != "imagery" else 120
        cues = _cues_for_block(manifest, stim_set)
        if run_type == "attention":
            savemat(
                design_dir / f"{run_label}_dm.mat",
                {
                    "dm": np.zeros((0, len(cues)), dtype=np.float64),
                    "condit_list": np.array(cues, dtype=object),
                },
            )
        else:
            _write_dm(design_dir / f"{run_label}_dm.mat", rows, cues)

    n_img = design_trial_count(design_dir)
    assert n_img is not None
    beta_dir = imagery / "betas" / "subj01" / "func1pt8mm" / "nsdimagerybetas_fithrf"
    beta_dir.mkdir(parents=True)
    vol = synthetic_volume.astype(np.float32)
    with h5py.File(beta_dir / "betas_nsdimagery.hdf5", "w") as f:
        f.create_dataset(
            "betas",
            data=np.tile(vol[np.newaxis, ...], (n_img, 1, 1, 1)),
        )

    sess_dir = nsd / "betas" / "subj01" / "func1pt8mm" / "betas_fithrf"
    sess_dir.mkdir(parents=True)
    with h5py.File(sess_dir / "betas_session01.hdf5", "w") as f:
        f.create_dataset("betas", data=np.tile(vol[np.newaxis, ...], (10, 1, 1, 1)))
    nii_stack = np.tile(synthetic_volume[..., np.newaxis], (1, 1, 1, 10))
    nib.save(nib.Nifti1Image(nii_stack, np.eye(4)), sess_dir / "betas_session01.nii.gz")

    return root


def test_s1_smoke_writes_under_smoke(s1_layout, monkeypatch):
    monkeypatch.setenv("MIRAGE_ABLATION_REPO", str(s1_layout))
    monkeypatch.setenv("MIRAGE_ABLATION_DATA_ROOT", str(s1_layout / "data"))
    monkeypatch.setenv("MIRAGE_ABLATION_RUNS_ROOT", str(s1_layout / "runs"))
    manifest = s1_layout / "manifests" / "nsd_imagery_test_manifest_v1.json"
    code = main(
        [
            "--stage",
            "S1",
            "--manifest",
            str(manifest),
            "--subject",
            "1",
            "--beta-version",
            "betas_fithrf",
            "--sessions",
            "1-1",
            "--overwrite",
        ]
    )
    assert code == 0
    paths = resolve_s1_paths(1, smoke=True)
    assert str(paths.out_dir).startswith(str(smoke_root()))
    assert paths.perception_h5.is_file()


def test_s1_refuses_overwrite(s1_layout, monkeypatch):
    monkeypatch.setenv("MIRAGE_ABLATION_REPO", str(s1_layout))
    monkeypatch.setenv("MIRAGE_ABLATION_DATA_ROOT", str(s1_layout / "data"))
    monkeypatch.setenv("MIRAGE_ABLATION_RUNS_ROOT", str(s1_layout / "runs"))
    manifest = s1_layout / "manifests" / "nsd_imagery_test_manifest_v1.json"
    args = [
        "--stage",
        "S1",
        "--manifest",
        str(manifest),
        "--subject",
        "1",
        "--beta-version",
        "betas_fithrf",
        "--sessions",
        "1-1",
        "--overwrite",
    ]
    assert main(args) == 0
    assert main(args[:-1]) != 0


def test_interrupted_write_leaves_no_final_h5(s1_layout, monkeypatch):
    from mirage_ablation.ingest import s1_run

    monkeypatch.setenv("MIRAGE_ABLATION_REPO", str(s1_layout))
    monkeypatch.setenv("MIRAGE_ABLATION_DATA_ROOT", str(s1_layout / "data"))
    monkeypatch.setenv("MIRAGE_ABLATION_RUNS_ROOT", str(s1_layout / "runs"))
    manifest = _valid_manifest()
    paths = resolve_s1_paths(1, smoke=True)
    if paths.perception_h5.is_file():
        paths.perception_h5.unlink()
    with pytest.raises(RuntimeError):
        s1_run.run_s1_subject(
            subject=1,
            beta_version="betas_fithrf",
            manifest=manifest,
            raw_nsd=s1_layout / "data" / "raw" / "nsd",
            raw_imagery=s1_layout / "data" / "raw" / "nsd_imagery",
            session_range=(1, 1),
            overwrite=True,
            run_id="test-abort",
            report_path=s1_layout / "runs" / "test-abort" / "s1_report.json",
            abort_after_perception_rows=1,
        )
    assert not paths.perception_h5.is_file()
