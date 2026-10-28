"""NSD-Imagery GLMsingle design blocks (720 beta rows)."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np

from mirage_ablation.ingest.mat_io import load_mat

TRs_PER_BETA: int = 60

RUN_BLOCK_SPECS: tuple[tuple[str, str, str], ...] = (
    ("visA", "vision", "A"),
    ("visB", "vision", "B"),
    ("visC", "vision", "C"),
    ("imgA_1", "imagery", "A"),
    ("imgA_2", "imagery", "A"),
    ("imgB_1", "imagery", "B"),
    ("imgB_2", "imagery", "B"),
    ("imgC_1", "imagery", "C"),
    ("imgC_2", "imagery", "C"),
    ("attA", "attention", "A"),
    ("attB", "attention", "B"),
    ("attC", "attention", "C"),
)


@dataclass(frozen=True)
class DesignMatrix:
    dm: np.ndarray
    condit_list: list[str]


def load_run_dm(design_dir: Path, run_label: str) -> DesignMatrix:
    path = design_dir / f"{run_label}_dm.mat"
    data = load_mat(path)
    if "dm" not in data:
        raise KeyError(f"dm missing in {path}")
    dm = np.asarray(data["dm"])
    raw_list = data.get("condit_list")
    if raw_list is None:
        raise KeyError(f"condit_list missing in {path}")
    condit_list = _normalize_condit_list(raw_list, _condit_cols(raw_list, dm), path)
    if dm.ndim == 1:
        if dm.size == 0:
            dm = np.zeros((0, len(condit_list)))
        else:
            raise ValueError(f"expected 2D dm in {path}, got {dm.shape}")
    elif dm.ndim != 2:
        raise ValueError(f"expected 2D dm in {path}, got {dm.shape}")
    if dm.shape[1] != len(condit_list):
        raise ValueError(
            f"condit_list length {len(condit_list)} != dm columns {dm.shape[1]} in {path}"
        )
    return DesignMatrix(dm=dm, condit_list=condit_list)


def _condit_cols(raw_list: object, dm: np.ndarray) -> int:
    if dm.ndim == 2:
        return dm.shape[1]
    arr = np.asarray(raw_list, dtype=object)
    return int(arr.reshape(-1).size)


def betas_per_run(dm: np.ndarray) -> int:
    return int((dm.shape[0] * dm.shape[1]) // TRs_PER_BETA)


def betas_per_column(dm: np.ndarray) -> int:
    if dm.shape[0] == 0:
        return 0
    if dm.shape[0] % TRs_PER_BETA != 0:
        raise ValueError(f"dm rows {dm.shape[0]} not divisible by {TRs_PER_BETA}")
    return dm.shape[0] // TRs_PER_BETA


def design_trial_count(design_dir: Path) -> int | None:
    total = 0
    found = False
    for run_label, _, _ in RUN_BLOCK_SPECS:
        path = design_dir / f"{run_label}_dm.mat"
        if not path.is_file():
            continue
        dm = load_run_dm(design_dir, run_label).dm
        total += betas_per_run(dm)
        found = True
    return total if found else None


def _normalize_condit_list(raw: object, n_cols: int, path: Path) -> list[str]:
    if raw is None:
        raise KeyError(f"condit_list missing in {path}")
    arr = np.asarray(raw, dtype=object)
    if arr.ndim == 0:
        items = [arr.item()]
    else:
        items = list(arr.reshape(-1))
    if len(items) != n_cols:
        raise ValueError(
            f"condit_list length {len(items)} != dm columns {n_cols} in {path}"
        )
    return [_condit_entry_to_cue(x) for x in items]


def _condit_entry_to_cue(entry: object) -> str:
    if entry is None:
        raise ValueError("empty condit_list entry")
    if isinstance(entry, bytes):
        text = entry.decode("utf-8", errors="replace")
    elif isinstance(entry, str):
        text = entry
    else:
        text = str(np.asarray(entry).squeeze())
    text = text.strip()
    if not text:
        raise ValueError("empty condit_list string")
    # NSD-Imagery cues are single letters; attention pairs may be two letters.
    return text[0].upper() if len(text) == 1 else text[0].upper()
