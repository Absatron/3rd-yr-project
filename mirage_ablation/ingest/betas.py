"""Mask and beta readers for S1 (MIRAGE-aligned scaling)."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterator

import h5py
import nibabel as nib
import numpy as np

from mirage_ablation.config.paths import (
    imagery_beta_h5,
    nsdgeneral_roi,
    perception_beta_session_h5,
    perception_beta_session_nii,
)

DEFAULT_VOXEL_ORDER: tuple[int, int, int] = (2, 1, 0)
SCALE_DIVISOR: float = 300.0


@dataclass(frozen=True)
class Mask:
    nsdgeneral_bool: np.ndarray
    flat_index: np.ndarray
    voxel_count: int
    voxel_order: tuple[int, int, int]
    mask_sha256: str


def load_nsdgeneral(
    subject: int,
    *,
    voxel_order: tuple[int, int, int] = DEFAULT_VOXEL_ORDER,
) -> Mask:
    path = nsdgeneral_roi(subject)
    img = nib.load(path)
    data = np.asanyarray(img.dataobj)
    cleaned = np.nan_to_num(data)
    bool_mask = cleaned == 1.0
    flat_index = np.flatnonzero(bool_mask.reshape(-1)).astype(np.int64)
    import hashlib

    mask_sha = hashlib.sha256(bool_mask.tobytes()).hexdigest()
    return Mask(
        nsdgeneral_bool=bool_mask,
        flat_index=flat_index,
        voxel_count=int(flat_index.size),
        voxel_order=voxel_order,
        mask_sha256=mask_sha,
    )


def _masked_trial_vector(vol: np.ndarray, mask: Mask) -> np.ndarray:
    ordered = np.transpose(vol, mask.voxel_order)
    flat = ordered.reshape(-1)
    out = flat[mask.flat_index]
    if np.issubdtype(vol.dtype, np.integer):
        return (out.astype(np.float32) / SCALE_DIVISOR)
    return out.astype(np.float32)


def iter_session_betas(
    subject: int,
    session: int,
    beta_version: str,
    mask: Mask,
) -> Iterator[np.ndarray]:
    """Yield one (750, V) float32 array per session (generator — one session in memory)."""
    path = perception_beta_session_h5(subject, session, beta_version)
    with h5py.File(path, "r") as f:
        betas = f["betas"]
        n_trials = betas.shape[0]
        chunk = np.empty((n_trials, mask.voxel_count), dtype=np.float32)
        for t in range(n_trials):
            chunk[t] = _masked_trial_vector(np.asarray(betas[t]), mask)
        yield chunk


def read_imagery_betas(
    subject: int,
    beta_version: str,
    mask: Mask,
) -> np.ndarray:
    path = imagery_beta_h5(subject, beta_version)
    with h5py.File(path, "r") as f:
        betas = f["betas"]
        n_trials = betas.shape[0]
        out = np.empty((n_trials, mask.voxel_count), dtype=np.float32)
        for t in range(n_trials):
            out[t] = _masked_trial_vector(np.asarray(betas[t]), mask)
    return out


def parity_check_session_trial(
    subject: int,
    session: int,
    beta_version: str,
    mask: Mask,
    trial_indices: tuple[int, ...],
) -> dict[str, object]:
    """HDF5 masked vector vs NIfTI dataobj slice (parity only)."""
    h5_path = perception_beta_session_h5(subject, session, beta_version)
    nii_path = perception_beta_session_nii(subject, session, beta_version)
    img = nib.load(nii_path)
    results: dict[str, object] = {"trials": {}, "pass": True}
    with h5py.File(h5_path, "r") as f:
        betas = f["betas"]
        for t in trial_indices:
            h5_vec = _masked_trial_vector(np.asarray(betas[t]), mask)
            nii_slice = np.asanyarray(img.dataobj[..., t])
            nii_vec = _masked_trial_vector(nii_slice, mask)
            ok = h5_vec.shape == nii_vec.shape and np.allclose(
                h5_vec, nii_vec, equal_nan=True
            )
            results["trials"][str(t)] = {"match": bool(ok)}
            if not ok:
                results["pass"] = False
    return results
