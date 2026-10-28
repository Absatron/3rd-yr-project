"""S1 stage writer (HDF5 + parquet + reports)."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable

import h5py
import numpy as np
import pandas as pd

from mirage_ablation.config.paths import betas_dir, smoke_root
from mirage_ablation.config.schema import NsdImageryTestManifest
from mirage_ablation.config.subjects import SESSIONS, TRIALS_PER_SESSION
from mirage_ablation.ingest.betas import (
    DEFAULT_VOXEL_ORDER,
    iter_session_betas,
    load_nsdgeneral,
    parity_check_session_trial,
    read_imagery_betas,
)
from mirage_ablation.ingest.imagery_trials import build_imagery_trials
from mirage_ablation.ingest.nsd_trials import build_perception_trials
from mirage_ablation.provenance import git_commit_short


@dataclass
class S1Paths:
    out_dir: Path
    perception_h5: Path
    imagery_h5: Path
    perception_parquet: Path
    imagery_parquet: Path
    mask_npz: Path


def resolve_s1_paths(subject: int, *, smoke: bool) -> S1Paths:
    out = (smoke_root() / f"subj{subject:02d}") if smoke else betas_dir(subject)
    return S1Paths(
        out_dir=out,
        perception_h5=out / "perception.h5",
        imagery_h5=out / "imagery.h5",
        perception_parquet=out / "perception_trials.parquet",
        imagery_parquet=out / "imagery_trials.parquet",
        mask_npz=out / "mask.npz",
    )


def s1_outputs_exist(paths: S1Paths) -> bool:
    return any(
        p.is_file()
        for p in (
            paths.perception_h5,
            paths.imagery_h5,
            paths.perception_parquet,
            paths.imagery_parquet,
            paths.mask_npz,
        )
    )


def _session_trial_count(subject: int, session: int, beta_version: str) -> int:
    from mirage_ablation.config.paths import perception_beta_session_h5

    path = perception_beta_session_h5(subject, session, beta_version)
    with h5py.File(path, "r") as f:
        return int(f["betas"].shape[0])


def run_s1_subject(
    *,
    subject: int,
    beta_version: str,
    manifest: NsdImageryTestManifest,
    raw_nsd: Path,
    raw_imagery: Path,
    session_range: tuple[int, int] | None,
    overwrite: bool,
    run_id: str,
    report_path: Path,
    on_perception_row: Callable[[], None] | None = None,
    abort_after_perception_rows: int | None = None,
) -> dict[str, object]:
    smoke = session_range is not None
    paths = resolve_s1_paths(subject, smoke=smoke)
    if s1_outputs_exist(paths) and not overwrite:
        raise FileExistsError(f"S1 outputs exist under {paths.out_dir} (use --overwrite)")

    n_sessions = SESSIONS[subject]
    if session_range is not None:
        lo, hi = session_range
        sessions = list(range(lo, hi + 1))
    else:
        sessions = list(range(1, n_sessions + 1))

    stim_csv = raw_nsd / "experiments" / "nsd" / "nsd_stim_info_merged.csv"
    expdesign = raw_nsd / "experiments" / "nsd" / "nsd_expdesign.mat"
    responses = raw_nsd / "ppdata" / f"subj{subject:02d}" / "behav" / "responses.tsv"
    design_dir = raw_imagery / "experiments" / "nsdimagery"
    cue_xlsx = design_dir / "cue_pair_list.xlsx"

    perception_trials = build_perception_trials(
        subject, stim_csv, expdesign, responses, n_sessions
    )
    if session_range is not None:
        lo, hi = session_range
        lo_g = (lo - 1) * TRIALS_PER_SESSION
        hi_g = hi * TRIALS_PER_SESSION
        perception_trials = perception_trials[
            (perception_trials["global_trial_index"] >= lo_g)
            & (perception_trials["global_trial_index"] < hi_g)
        ].reset_index(drop=True)

    imagery_trials = build_imagery_trials(subject, design_dir, cue_xlsx, manifest)
    mask = load_nsdgeneral(subject, voxel_order=DEFAULT_VOXEL_ORDER)
    paths.out_dir.mkdir(parents=True, exist_ok=True)

    tmp_perception = paths.perception_h5.with_name(f"{paths.perception_h5.name}.tmp")
    tmp_imagery = paths.imagery_h5.with_name(f"{paths.imagery_h5.name}.tmp")
    tmp_perception_parquet = paths.perception_parquet.with_name(
        f"{paths.perception_parquet.name}.tmp"
    )
    tmp_imagery_parquet = paths.imagery_parquet.with_name(
        f"{paths.imagery_parquet.name}.tmp"
    )
    tmp_mask = paths.mask_npz.parent / f"{paths.mask_npz.stem}.tmp.npz"

    perception_trials.to_parquet(tmp_perception_parquet, index=False)
    imagery_trials.to_parquet(tmp_imagery_parquet, index=False)
    np.savez_compressed(
        tmp_mask,
        nsdgeneral_bool=mask.nsdgeneral_bool,
        flat_index=mask.flat_index,
        voxel_count=mask.voxel_count,
    )

    rows_written = 0
    with h5py.File(tmp_perception, "w") as out_f:
        ds = out_f.create_dataset(
            "betas",
            shape=(len(perception_trials), mask.voxel_count),
            dtype=np.float32,
            chunks=(min(64, max(1, len(perception_trials))), mask.voxel_count),
            fillvalue=np.nan,
        )
        out_row = 0
        for session in sessions:
            for chunk in iter_session_betas(subject, session, beta_version, mask):
                if session_range is not None:
                    session_rows = perception_trials[
                        perception_trials["session_id"] == session
                    ]
                    for _, row in session_rows.iterrows():
                        t_idx = int(row["trial_in_session"]) - 1
                        ds[out_row] = chunk[t_idx]
                        out_row += 1
                        rows_written += 1
                        if on_perception_row:
                            on_perception_row()
                        if (
                            abort_after_perception_rows is not None
                            and rows_written >= abort_after_perception_rows
                        ):
                            raise RuntimeError("abort_after_perception_rows")
                else:
                    n = chunk.shape[0]
                    ds[out_row : out_row + n] = chunk
                    out_row += n
                    rows_written += n
                    if on_perception_row:
                        on_perception_row()
        ds.attrs["beta_version"] = beta_version
        ds.attrs["scale_divisor"] = 300
        ds.attrs["mask_sha256"] = mask.mask_sha256
        ds.attrs["voxel_order"] = list(mask.voxel_order)
        ds.attrs["n_sessions"] = len(sessions) if smoke else n_sessions
        ds.attrs["git_commit"] = git_commit_short() or ""
        ds.attrs["run_id"] = run_id

    imagery = read_imagery_betas(subject, beta_version, mask)
    with h5py.File(tmp_imagery, "w") as out_f:
        ids = out_f.create_dataset(
            "betas",
            data=imagery,
            dtype=np.float32,
            chunks=(min(64, imagery.shape[0]), mask.voxel_count),
        )
        ids.attrs["beta_version"] = beta_version
        ids.attrs["scale_divisor"] = 300
        ids.attrs["mask_sha256"] = mask.mask_sha256
        ids.attrs["voxel_order"] = list(mask.voxel_order)
        ids.attrs["git_commit"] = git_commit_short() or ""
        ids.attrs["run_id"] = run_id

    with h5py.File(tmp_perception, "r") as f:
        nan_perception = int(np.isnan(np.asarray(f["betas"])).sum())
    with h5py.File(tmp_imagery, "r") as f:
        nan_imagery = int(np.isnan(np.asarray(f["betas"])).sum())

    parity_trials = tuple(
        t for t in (0, 374, 749) if t < _session_trial_count(subject, 1, beta_version)
    )
    parity = (
        parity_check_session_trial(
            subject, 1, beta_version, mask, parity_trials
        )
        if parity_trials
        else {"pass": True, "skipped": "session too short for parity probes"}
    )

    report: dict[str, object] = {
        "subject": subject,
        "beta_version": beta_version,
        "smoke": smoke,
        "session_range": list(session_range) if session_range else None,
        "perception_rows": int(len(perception_trials)),
        "imagery_rows": int(len(imagery_trials)),
        "voxel_count": mask.voxel_count,
        "nan_perception": nan_perception,
        "nan_imagery": nan_imagery,
        "parity_session1": parity,
        "pass": nan_perception == 0
        and nan_imagery == 0
        and parity.get("pass") is True,
        "finished_at": datetime.now(timezone.utc).isoformat(),
    }
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2))

    os.replace(tmp_perception, paths.perception_h5)
    os.replace(tmp_imagery, paths.imagery_h5)
    os.replace(tmp_perception_parquet, paths.perception_parquet)
    os.replace(tmp_imagery_parquet, paths.imagery_parquet)
    os.replace(tmp_mask, paths.mask_npz)

    return report
