"""Load MATLAB design files (v7 or v7.3)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import h5py
import numpy as np
from scipy.io import loadmat


def load_mat(path: Path) -> dict[str, Any]:
    """Return top-level arrays from a .mat file."""
    try:
        return loadmat(path, simplify_cells=True)
    except NotImplementedError:
        out: dict[str, Any] = {}
        with h5py.File(path, "r") as f:
            for key in f.keys():
                out[key] = np.asarray(f[key])
        return out
