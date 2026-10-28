"""NSD perception trial table (three-source reconciliation)."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from mirage_ablation.config.subjects import TRIALS_PER_SESSION
from mirage_ablation.ingest.mat_io import load_mat


class TrialReconciliationError(RuntimeError):
    """Raised when CSV, expdesign, and responses disagree."""


def build_perception_trials(
    subject: int,
    stim_csv: Path,
    expdesign_mat: Path,
    responses_tsv: Path,
    n_sessions: int,
) -> pd.DataFrame:
    stim_df = pd.read_csv(stim_csv)
    exp = load_mat(expdesign_mat)
    masterordering = np.asarray(exp["masterordering"]).reshape(-1)
    subjectim = np.asarray(exp["subjectim"])

    resp = pd.read_csv(responses_tsv, sep="\t")
    resp = resp[resp["SUBJECT"] == subject].copy()
    resp = resp.sort_values(["SESSION", "TRIAL"])

    max_trials = n_sessions * TRIALS_PER_SESSION
    rows: list[dict[str, object]] = []

    subj_col = f"subject{subject}"
    rep_cols = [f"subject{subject}_rep{j}" for j in range(3)]

    for _, r in resp.iterrows():
        session_id = int(r["SESSION"])
        if session_id < 1 or session_id > n_sessions:
            continue
        trial_in_session = int(r["TRIAL"])
        if trial_in_session < 1 or trial_in_session > TRIALS_PER_SESSION:
            raise TrialReconciliationError(
                f"subject {subject} session {session_id} trial {trial_in_session} out of range"
            )
        global_trial_index = (session_id - 1) * TRIALS_PER_SESSION + (
            trial_in_session - 1
        )
        if global_trial_index >= max_trials:
            continue

        nsd_from_resp = int(r["73KID"]) - 1
        mo_idx = int(masterordering[global_trial_index]) - 1
        sim = np.asarray(subjectim)
        if sim.ndim == 1:
            nsd_from_design = int(sim[mo_idx]) - 1
        else:
            nsd_from_design = int(sim[subject - 1, mo_idx]) - 1
        if nsd_from_resp != nsd_from_design:
            raise TrialReconciliationError(
                f"subject {subject} session {session_id} trial {trial_in_session}: "
                f"responses nsd_id {nsd_from_resp} != expdesign {nsd_from_design}"
            )

        csv_rows = stim_df[stim_df["nsdId"] == nsd_from_resp]
        if csv_rows.empty:
            raise TrialReconciliationError(
                f"subject {subject} session {session_id} trial {trial_in_session}: "
                f"nsdId {nsd_from_resp} missing from stim CSV"
            )
        csv_row = csv_rows.iloc[0]
        if csv_row.get(subj_col, 0) == 0:
            raise TrialReconciliationError(
                f"subject {subject} session {session_id} trial {trial_in_session}: "
                f"CSV marks nsdId {nsd_from_resp} as not shown to subject"
            )

        rep_index: int | None = None
        scan_one_based = global_trial_index + 1
        for ri, col in enumerate(rep_cols):
            val = csv_row[col]
            if pd.isna(val) or int(val) == 0:
                continue
            if int(val) == scan_one_based:
                rep_index = ri
                break
        if rep_index is None:
            raise TrialReconciliationError(
                f"subject {subject} session {session_id} trial {trial_in_session}: "
                f"scan id {scan_one_based} not in CSV rep columns for nsdId {nsd_from_resp}"
            )

        rows.append(
            {
                "subject_id": np.int8(subject),
                "session_id": np.int16(session_id),
                "run_id": np.int8(int(r["RUN"])),
                "trial_in_session": np.int16(trial_in_session),
                "global_trial_index": np.int32(global_trial_index),
                "nsd_id": np.int32(nsd_from_resp),
                "coco_image_id": np.int64(int(csv_row["cocoId"])),
                "shared1000": bool(str(csv_row.get("shared1000", "")).lower() == "true"),
                "rep_index": np.int8(rep_index),
            }
        )

    if not rows:
        raise TrialReconciliationError(f"subject {subject}: no perception trials built")

    df = pd.DataFrame(rows)
    df = df.sort_values("global_trial_index").reset_index(drop=True)
    expected = np.arange(len(df), dtype=np.int32)
    if not np.array_equal(df["global_trial_index"].to_numpy(), expected):
        raise TrialReconciliationError(
            f"subject {subject}: global_trial_index not contiguous from 0"
        )
    if not df["rep_index"].isin([0, 1, 2]).all():
        raise TrialReconciliationError(f"subject {subject}: invalid rep_index values")
    return df


def drop_unacquired_csv_scan_ids(
    subject: int, stim_csv: Path, n_sessions: int
) -> set[int]:
    """Scan IDs from CSV rep columns, excluding unacquired (MIRAGE R4)."""
    stim_df = pd.read_csv(stim_csv)
    subj_col = f"subject{subject}"
    rep_cols = [f"subject{subject}_rep{j}" for j in range(3)]
    subj_rows = stim_df[stim_df[subj_col] != 0]
    max_scan = n_sessions * TRIALS_PER_SESSION
    scan_ids: set[int] = set()
    for _, row in subj_rows.iterrows():
        for col in rep_cols:
            val = row[col]
            if pd.isna(val) or int(val) == 0:
                continue
            scan_zero = int(val) - 1
            if scan_zero < 0 or scan_zero >= max_scan:
                continue
            scan_ids.add(scan_zero)
    return scan_ids
