"""Unit tests for NSD perception trial builder (T-010)."""

from __future__ import annotations

import numpy as np
import pytest
from scipy.io import savemat

from mirage_ablation.ingest.nsd_trials import (
    TrialReconciliationError,
    build_perception_trials,
    drop_unacquired_csv_scan_ids,
)


@pytest.fixture
def perception_fixture(tmp_path):
    stim = tmp_path / "nsd_stim_info_merged.csv"
    stim.write_text(
        "cocoId,nsdId,shared1000,subject1,subject1_rep0,subject1_rep1,subject1_rep2\n"
        "1001,10,False,1,1,2,99999\n"
        "1002,11,True,1,0,2,0\n"
    )
    exp = tmp_path / "nsd_expdesign.mat"
    savemat(
        exp,
        {
            "masterordering": np.array([[1, 2]], dtype=np.float64),
            "subjectim": np.array([[11, 12], [11, 12]], dtype=np.float64),
        },
    )
    resp = tmp_path / "responses.tsv"
    resp.write_text(
        "SUBJECT\tSESSION\tRUN\tTRIAL\t73KID\t10KID\n"
        "1\t1\t1\t1\t11\t1\n"
        "1\t1\t1\t2\t12\t2\n"
    )
    return stim, exp, resp


def test_unacquired_rep_dropped_from_csv_scan_set(perception_fixture):
    stim, _, _ = perception_fixture
    scans = drop_unacquired_csv_scan_ids(1, stim, n_sessions=1)
    assert scans == {0, 1}


def test_reconciliation_mismatch_raises(perception_fixture):
    stim, exp, resp = perception_fixture
    resp.write_text(
        "SUBJECT\tSESSION\tRUN\tTRIAL\t73KID\t10KID\n"
        "1\t1\t1\t1\t99\t1\n"
    )
    with pytest.raises(TrialReconciliationError) as exc:
        build_perception_trials(1, stim, exp, resp, n_sessions=1)
    assert "session 1" in str(exc.value)


def test_global_trial_index_contiguous(perception_fixture):
    stim, exp, resp = perception_fixture
    df = build_perception_trials(1, stim, exp, resp, n_sessions=1)
    assert len(df) == 2
    assert df["global_trial_index"].tolist() == [0, 1]
    assert set(df["rep_index"].tolist()) <= {0, 1, 2}
