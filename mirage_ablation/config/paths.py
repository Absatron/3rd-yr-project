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
