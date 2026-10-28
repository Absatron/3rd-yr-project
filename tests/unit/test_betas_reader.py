"""Unit tests for mask and beta readers (T-012)."""

from __future__ import annotations

from pathlib import Path

import h5py
import nibabel as nib
import numpy as np
import pytest

from mirage_ablation.ingest.betas import (
    SCALE_DIVISOR,
    iter_session_betas,
    load_nsdgeneral,
)


@pytest.fixture
def int16_betas(tmp_path, synthetic_volume, synthetic_nsdgeneral_nii, monkeypatch):
    """Session HDF5 int16 + matching NIfTI (voxel order 0,1,2 default)."""
    monkeypatch.setenv("MIRAGE_ABLATION_DATA_ROOT", str(tmp_path / "data"))
    root = tmp_path / "data" / "raw" / "nsd"
    roi = root / "ppdata" / "subj01" / "func1pt8mm" / "roi"
    roi.mkdir(parents=True)
    betas_dir = root / "betas" / "subj01" / "func1pt8mm" / "betas_fithrf"
    betas_dir.mkdir(parents=True)

    import shutil

    shutil.copy(synthetic_nsdgeneral_nii, roi / "nsdgeneral.nii.gz")

    vol = synthetic_volume.astype(np.int16) * 300
    trials = 10
    stack = np.tile(vol[np.newaxis, ...], (trials, 1, 1, 1))
    h5_path = betas_dir / "betas_session01.hdf5"
    with h5py.File(h5_path, "w") as f:
        f.create_dataset("betas", data=stack)

    nii_stack = np.tile(synthetic_volume[..., np.newaxis], (1, 1, 1, trials))
    nii_path = betas_dir / "betas_session01.nii.gz"
    nib.save(nib.Nifti1Image(nii_stack.astype(np.float32), np.eye(4)), nii_path)
    return tmp_path


def test_int16_scaling_exact(int16_betas):
    mask = load_nsdgeneral(1, voxel_order=(0, 1, 2))
    chunk = next(iter_session_betas(1, 1, "betas_fithrf", mask))
    with h5py.File(
        int16_betas
        / "data/raw/nsd/betas/subj01/func1pt8mm/betas_fithrf/betas_session01.hdf5",
        "r",
    ) as f:
        raw = np.asarray(f["betas"][0])
    expected = float(raw.reshape(-1)[mask.flat_index[0]]) / SCALE_DIVISOR
    assert chunk[0, 0] == pytest.approx(expected)


def test_hdf5_nifti_masked_match(int16_betas):
    from mirage_ablation.ingest.betas import parity_check_session_trial

    mask = load_nsdgeneral(1, voxel_order=(0, 1, 2))
    result = parity_check_session_trial(1, 1, "betas_fithrf", mask, (0, 1))
    assert result["pass"] is True


def test_mask_excludes_minus_one(tmp_path, monkeypatch):
    monkeypatch.setenv("MIRAGE_ABLATION_DATA_ROOT", str(tmp_path / "data"))
    root = tmp_path / "data" / "raw" / "nsd" / "ppdata" / "subj01" / "func1pt8mm" / "roi"
    root.mkdir(parents=True)
    data = np.zeros((4, 5, 6), dtype=np.float32)
    data[0, 0, 0] = -1.0
    data[1, 1, 1] = 1.0
    nib.save(nib.Nifti1Image(data, np.eye(4)), root / "nsdgeneral.nii.gz")
    mask = load_nsdgeneral(1)
    assert mask.voxel_count == 1
    assert not mask.nsdgeneral_bool[0, 0, 0]


def test_generator_yields_one_session_only(int16_betas):
    mask = load_nsdgeneral(1, voxel_order=(0, 1, 2))
    gen = iter_session_betas(1, 1, "betas_fithrf", mask)
    first = next(gen)
    with pytest.raises(StopIteration):
        next(gen)
    assert first.shape == (10, mask.voxel_count)
