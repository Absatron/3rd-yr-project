"""Synthetic NSD-like fixtures (generated at test time; no binary blobs in git)."""

from __future__ import annotations

from pathlib import Path

import h5py
import nibabel as nib
import numpy as np
import pytest
from scipy.io import savemat


@pytest.fixture
def repo_layout(tmp_path, monkeypatch):
    """Minimal repo + data roots for path/provenance tests."""
    monkeypatch.setenv("MIRAGE_ABLATION_REPO", str(tmp_path))
    monkeypatch.setenv("MIRAGE_ABLATION_DATA_ROOT", str(tmp_path / "data"))
    (tmp_path / "manifests").mkdir(parents=True)
    (tmp_path / "runs").mkdir(parents=True)
    return tmp_path


@pytest.fixture
def synthetic_volume(tmp_path):
    """4×5×6 float32 volume for NIfTI/HDF5 parity tests."""
    vol = np.arange(4 * 5 * 6, dtype=np.float32).reshape(4, 5, 6)
    return vol


@pytest.fixture
def synthetic_nsdgeneral_nii(tmp_path, synthetic_volume):
    """nsdgeneral mask with values {-1, 0, 1}."""
    data = np.zeros((4, 5, 6), dtype=np.float32)
    data[0, 0, 0] = -1.0
    data[1, 1, 1] = 1.0
    data[2, 2, 2] = 1.0
    path = tmp_path / "nsdgeneral.nii.gz"
    img = nib.Nifti1Image(data, np.eye(4))
    nib.save(img, path)
    return path


@pytest.fixture
def synthetic_session_h5(tmp_path, synthetic_volume):
    """Two sessions × 10 trials float32 betas (trial, x, y, z), percent signal change scale."""
    path = tmp_path / "betas_session01.hdf5"
    trials = 10
    stack = np.tile(synthetic_volume[np.newaxis, ...], (trials, 1, 1, 1)).astype(np.float32)
    with h5py.File(path, "w") as f:
        f.create_dataset("betas", data=stack, chunks=(1, 4, 5, 6))
    return path


@pytest.fixture
def synthetic_stim_csv(tmp_path):
    path = tmp_path / "nsd_stim_info_merged.csv"
    path.write_text(
        "cocoId,nsdId,shared1000,subject1_rep0,subject1_rep1,subject1_rep2\n"
        "1001,10,False,1,2,99999\n"
        "2002,20,True,0,0,0\n"
    )
    return path


@pytest.fixture
def synthetic_responses_tsv(tmp_path):
    path = tmp_path / "responses.tsv"
    path.write_text(
        "SUBJECT\tSESSION\tRUN\tTRIAL\t73KID\t10KID\n"
        "1\t1\t1\t1\t11\t1\n"
        "1\t1\t1\t2\t12\t2\n"
    )
    return path


@pytest.fixture
def synthetic_expdesign_mat(tmp_path):
    path = tmp_path / "nsd_expdesign.mat"
    savemat(path, {"masterordering": np.array([[1, 2]], dtype=np.float64)})
    return path


@pytest.fixture
def synthetic_mat_v73(tmp_path):
    """MATLAB v7.3-style HDF5 .mat (scipy.io.loadmat cannot read)."""
    path = tmp_path / "design_v73.mat"
    with h5py.File(path, "w") as f:
        f.create_dataset("dummy", data=np.array([1.0, 2.0]))
    return path


@pytest.fixture
def synthetic_nii_betas(tmp_path, synthetic_volume):
    """4D NIfTI (x, y, z, t) matching synthetic_session_h5 trial order."""
    trials = 10
    stack = np.tile(synthetic_volume[..., np.newaxis], (1, 1, 1, trials))
    path = tmp_path / "betas_session01.nii.gz"
    img = nib.Nifti1Image(stack.astype(np.float32), np.eye(4))
    nib.save(img, path)
    return path
