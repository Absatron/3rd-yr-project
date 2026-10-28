"""Resolve data roots for laptop vs CSF scratch."""

from __future__ import annotations

import os
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]


def repo_root() -> Path:
    return Path(os.environ.get("MIRAGE_ABLATION_REPO", _REPO_ROOT))


def data_root() -> Path:
    """Project data directory (symlink scratch on CSF when batch jobs run)."""
    env = os.environ.get("MIRAGE_ABLATION_DATA_ROOT")
    if env:
        return Path(env)
    return repo_root() / "data"


def raw_nsd_dir() -> Path:
    return data_root() / "raw" / "nsd"


def raw_nsd_imagery_dir() -> Path:
    return data_root() / "raw" / "nsd_imagery"


def frozen_weights_dir() -> Path:
    return data_root() / "frozen_weights"


def frozen_catalogues_dir() -> Path:
    return data_root() / "frozen_catalogues"


def manifests_dir() -> Path:
    return repo_root() / "manifests"


def processed_dir() -> Path:
    return data_root() / "processed"


def betas_dir(subj: int) -> Path:
    return processed_dir() / "betas" / f"subj{subj:02d}"


def betas_masked_dir(subj: int) -> Path:
    return processed_dir() / "betas_masked" / f"subj{subj:02d}"


def targets_dir() -> Path:
    return processed_dir() / "targets"


def splits_dir(manifest_sha: str, setting: str) -> Path:
    setting_key = f"setting_{setting.lower()}"
    return processed_dir() / "splits" / manifest_sha / setting_key


def smoke_root() -> Path:
    return processed_dir() / "_smoke"


def runs_dir() -> Path:
    env = os.environ.get("MIRAGE_ABLATION_RUNS_ROOT")
    if env:
        return Path(env)
    dr = data_root()
    if dr.name == "data":
        return dr.parent / "runs"
    return repo_root() / "runs"


def manifest_sha_short(full_sha256: str) -> str:
    return full_sha256[:12]


def perception_beta_session_h5(
    subject: int, session: int, beta_version: str
) -> Path:
    return (
        raw_nsd_dir()
        / "betas"
        / f"subj{subject:02d}"
        / "func1pt8mm"
        / beta_version
        / f"betas_session{session:02d}.hdf5"
    )


def imagery_beta_h5(subject: int, beta_version: str) -> Path:
    imagery_dir = f"nsdimagery{beta_version}"
    return (
        raw_nsd_imagery_dir()
        / "betas"
        / f"subj{subject:02d}"
        / "func1pt8mm"
        / imagery_dir
        / "betas_nsdimagery.hdf5"
    )


def nsdgeneral_roi(subject: int) -> Path:
    return (
        raw_nsd_dir()
        / "ppdata"
        / f"subj{subject:02d}"
        / "func1pt8mm"
        / "roi"
        / "nsdgeneral.nii.gz"
    )


def perception_beta_session_nii(subject: int, session: int, beta_version: str) -> Path:
    return (
        raw_nsd_dir()
        / "betas"
        / f"subj{subject:02d}"
        / "func1pt8mm"
        / beta_version
        / f"betas_session{session:02d}.nii.gz"
    )
