"""Real-data S1 smoke + trial reconciliation (T-015, CSF only)."""

from __future__ import annotations

from pathlib import Path

import pytest

from mirage_ablation.config.paths import manifests_dir, raw_nsd_dir, raw_nsd_imagery_dir
from mirage_ablation.config.schema import NsdImageryTestManifest
from mirage_ablation.config.subjects import SESSIONS, TRIALS_PER_SESSION
from mirage_ablation.ingest.imagery_design import design_trial_count
from mirage_ablation.ingest.imagery_trials import build_imagery_trials
from mirage_ablation.ingest.nsd_trials import build_perception_trials
from mirage_ablation.ingest.cli import main


pytestmark = pytest.mark.csf_data


def _manifest() -> NsdImageryTestManifest:
    path = manifests_dir() / "nsd_imagery_test_manifest_v1.json"
    return NsdImageryTestManifest.model_validate_json(path.read_text())


@pytest.fixture(scope="module")
def require_scratch_data():
    stim = raw_nsd_dir() / "experiments" / "nsd" / "nsd_stim_info_merged.csv"
    if not stim.is_file():
        pytest.skip("NSD metadata not on MIRAGE_ABLATION_DATA_ROOT")


def test_trial_tables_all_subjects(require_scratch_data):
    manifest = _manifest()
    design_dir = raw_nsd_imagery_dir() / "experiments" / "nsdimagery"
    cue_xlsx = design_dir / "cue_pair_list.xlsx"
    expected_img = design_trial_count(design_dir)
    assert expected_img == 720
    for subject in SESSIONS:
        n_sess = SESSIONS[subject]
        stim = raw_nsd_dir() / "experiments" / "nsd" / "nsd_stim_info_merged.csv"
        exp = raw_nsd_dir() / "experiments" / "nsd" / "nsd_expdesign.mat"
        resp = raw_nsd_dir() / "ppdata" / f"subj{subject:02d}" / "behav" / "responses.tsv"
        perc = build_perception_trials(subject, stim, exp, resp, n_sess)
        assert len(perc) == n_sess * TRIALS_PER_SESSION
        img = build_imagery_trials(subject, design_dir, cue_xlsx, manifest)
        assert len(img) == expected_img
        imagery_only = img[img["run_type"] == "imagery"]
        assert imagery_only["stimulus_id"].nunique() == 18
        for _, grp in imagery_only.groupby("stimulus_id"):
            assert len(grp) == 16


def test_s1_smoke_subj01_sessions_1_2(require_scratch_data):
    manifest_path = manifests_dir() / "nsd_imagery_test_manifest_v1.json"
    code = main(
        [
            "--stage",
            "S1",
            "--manifest",
            str(manifest_path),
            "--subject",
            "1",
            "--beta-version",
            "betas_fithrf",
            "--sessions",
            "1-2",
            "--overwrite",
        ]
    )
    assert code == 0
