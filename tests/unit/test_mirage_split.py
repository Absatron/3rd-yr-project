"""Unit tests for MIRAGE training-split cross-check."""

from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

import pytest

from mirage_ablation.s0.mirage_split import build_mirage_split_verification


def _write_stim_csv(path: Path) -> None:
    path.write_text(
        "cocoId,nsdId,shared1000,subject1,subject2\n"
        "999001,100,False,1,0\n"
        "353830,30857,False,0,1\n"
        "888002,200,True,1,1\n"
    )


@pytest.fixture
def mini_manifest():
    return SimpleNamespace(
        imagery_stimuli=[
            SimpleNamespace(
                stimulus_id="complex_nsd30857",
                type="complex",
                coco_id=353830,
                nsd_id=30857,
                overlap_label="shared1000",
            ),
            SimpleNamespace(
                stimulus_id="complex_nsd00100",
                type="complex",
                coco_id=999001,
                nsd_id=100,
                overlap_label="shared1000",
            ),
        ],
    )


def test_mirage_split_agrees_with_audit(tmp_path, mini_manifest):
    stim = tmp_path / "nsd_stim_info_merged.csv"
    _write_stim_csv(stim)
    out = build_mirage_split_verification(mini_manifest, stim)
    assert out["all_subjects_agree"] is True
    subj2 = out["per_subject"]["2"]
    hit = next(c for c in subj2["comparisons"] if c["stimulus_id"] == "complex_nsd30857")
    assert hit["audit_exact_seen"] is True
    assert hit["mirage_nsd_in_train"] is True
    subj1 = out["per_subject"]["1"]
    other = next(c for c in subj1["comparisons"] if c["stimulus_id"] == "complex_nsd00100")
    assert other["audit_exact_seen"] is True
    assert other["mirage_nsd_in_train"] is True
