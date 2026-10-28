"""NSD-Imagery trial table aligned to 720 GLMsingle beta rows."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from mirage_ablation.config.schema import NsdImageryTestManifest
from mirage_ablation.ingest.imagery_design import (
    RUN_BLOCK_SPECS,
    betas_per_column,
    load_run_dm,
)
from mirage_ablation.s0.catalogue import _read_xlsx_rows


class UnknownLetterCueError(ValueError):
    """Cue letter cannot be mapped to the frozen manifest."""


def build_imagery_trials(
    subject: int,
    design_dir: Path,
    cue_xlsx: Path,
    manifest: NsdImageryTestManifest,
) -> pd.DataFrame:
    cue_by_letter = {s.letter_cue.upper(): s.stimulus_id for s in manifest.imagery_stimuli}
    _crosscheck_cue_xlsx(cue_xlsx, cue_by_letter)

    rows: list[dict[str, object]] = []
    beta_index = 0
    for run_label, run_type, stim_set in RUN_BLOCK_SPECS:
        block = load_run_dm(design_dir, run_label)
        per_col = betas_per_column(block.dm)
        if per_col == 0:
            continue
        for col_idx, cue_letter in enumerate(block.condit_list):
            stimulus_id: str | None
            if run_type == "attention":
                stimulus_id = None
            else:
                try:
                    stimulus_id = cue_by_letter[cue_letter.upper()]
                except KeyError as exc:
                    raise UnknownLetterCueError(
                        f"unknown letter cue {cue_letter!r} in {run_label}_dm column {col_idx}"
                    ) from exc
            for trial_in_run in range(1, per_col + 1):
                rows.append(
                    {
                        "subject_id": np.int8(subject),
                        "beta_index": np.int16(beta_index),
                        "run_label": run_label,
                        "run_type": run_type,
                        "stim_set": stim_set,
                        "trial_in_run": np.int16(trial_in_run),
                        "letter_cue": cue_letter.upper(),
                        "stimulus_id": stimulus_id,
                    }
                )
                beta_index += 1

    df = pd.DataFrame(rows)
    if df["beta_index"].tolist() != list(range(len(df))):
        raise RuntimeError("beta_index not contiguous")
    return df


def _crosscheck_cue_xlsx(cue_xlsx: Path, cue_by_letter: dict[str, str]) -> None:
    if not cue_xlsx.is_file():
        return
    rows = _read_xlsx_rows(cue_xlsx)
    for _, _, cue in rows[1:]:
        letter = cue.strip().upper()
        if letter and letter not in cue_by_letter:
            raise UnknownLetterCueError(
                f"cue_pair_list letter {letter!r} absent from manifest"
            )
