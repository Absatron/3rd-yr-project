"""Unit tests for NSD-Imagery trial builder (T-011, 720 beta rows)."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest
from scipy.io import savemat

from mirage_ablation.config.schema import NsdImageryTestManifest
from mirage_ablation.ingest.imagery_design import RUN_BLOCK_SPECS, design_trial_count
from mirage_ablation.ingest.imagery_trials import UnknownLetterCueError, build_imagery_trials


def _valid_manifest() -> NsdImageryTestManifest:
    from mirage_ablation.config.paths import manifests_dir

    path = manifests_dir() / "nsd_imagery_test_manifest_v1.json"
    if not path.is_file():
        pytest.skip("manifest not in repo")
    return NsdImageryTestManifest.model_validate_json(path.read_text())


def _write_dm(path: Path, rows: int, cues: list[str]) -> None:
    savemat(
        path,
        {
            "dm": np.ones((rows, len(cues)), dtype=np.float64),
            "condit_list": np.array(cues, dtype=object),
        },
    )


def _cues_for_block(manifest: NsdImageryTestManifest, stim_set: str) -> list[str]:
    type_map = {"A": "simple", "B": "complex", "C": "conceptual"}
    stype = type_map[stim_set]
    return [s.letter_cue for s in manifest.imagery_stimuli if s.type == stype]


@pytest.fixture
def design_dir(tmp_path):
    manifest = _valid_manifest()
    for run_label, run_type, stim_set in RUN_BLOCK_SPECS:
        if run_type == "vision":
            rows = 480
        elif run_type == "imagery":
            rows = 960
        else:
            rows = 0
        cues = _cues_for_block(manifest, stim_set)
        if rows == 0:
            savemat(
                tmp_path / f"{run_label}_dm.mat",
                {
                    "dm": np.zeros((0, len(cues)), dtype=np.float64),
                    "condit_list": np.array(cues, dtype=object),
                },
            )
        else:
            _write_dm(tmp_path / f"{run_label}_dm.mat", rows, cues)
    return tmp_path


def test_twelve_run_blocks_and_sixteen_imagery_reps(design_dir):
    manifest = _valid_manifest()
    df = build_imagery_trials(1, design_dir, design_dir / "missing.xlsx", manifest)
    assert df["run_label"].nunique() == 9
    assert len(df) == design_trial_count(design_dir) == 720
    imagery = df[df["run_type"] == "imagery"]
    for (_, _run), grp in imagery.groupby(["stimulus_id", "run_label"]):
        assert len(grp) == 16
    vision = df[df["run_type"] == "vision"]
    for sid, grp in vision.groupby("stimulus_id"):
        assert len(grp) == 8, sid


def test_unknown_cue_raises(design_dir):
    bad = design_dir / "visA_dm.mat"
    savemat(
        bad,
        {
            "dm": np.ones((480, 6)),
            "condit_list": np.array(["T", "W", "K", "B", "C", "Q"], dtype=object),
        },
    )
    manifest = _valid_manifest()
    with pytest.raises(UnknownLetterCueError):
        build_imagery_trials(1, design_dir, design_dir / "missing.xlsx", manifest)
