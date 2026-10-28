# Execution Log: M1 Shared Ingest Foundation (S1–S4, Track B) — IP-1 Foundation

**Date started:** 2026-10-28
**Date completed:** In progress (CSF verification pending)
**Implementation Plan:** `implementation_plans/2026-10-27-perception-imagery-latent-ablation-s1-s4-ingest-implementation-plan.md`
**Executor:** AI-assisted (execute-implementation-plan)
**Milestone scope:** IP-1 only (T-001, T-002, T-003, T-004, T-005, T-050; T-004b scripts)

---

## Pre-Execution Review

### Issues Identified Before Starting
- CSF `ssh -o BatchMode=yes csf3` returned `Permission denied (keyboard-interactive)` — Duo/ControlMaster not active for agent session. CSF sbatch, behav sync, env create, probe, and CSF pytest deferred to investigator handoff.

### Prerequisites Confirmed
- [x] Plan status: Approved with D1/D3/D4 in `runs/registry.yaml`
- [x] Laptop Python 3.11.5 available
- [ ] CSF BatchMode SSH (BLOCKED — user must `ssh -Y csf3` and approve Duo)
- [x] Manifest sidecars present in repo

---

## Task Execution Record

### T-001: Track B environment and lock file
- **Status:** PARTIAL (CSF job running)
- **Started:** 2026-10-28
- **Completed:** 2026-10-28 (laptop); CSF env BLOCKED
- **Verification result:**
  - Laptop: `.venv-track-b` Python 3.11.5; `pip install -r requirements-track-b.txt` OK
  - `configs/environments/track_b.lock` from venv `pip freeze` (CPU stack; CSF GPU freeze pending `create_track_b_env.sbatch`)
  - `scripts/csf/create_track_b_env.sbatch` added
  - CSF conda env + import probe: **not run** (SSH blocked)
- **Acceptance criteria met:**
  - [ ] CSF env import probe in job
  - [x] Laptop Python 3.11.x
  - [x] Lock committed; registry `environment_pins.track_b_python` updated
  - [x] Laptop venv + `python3 -m pytest tests/unit -q` green (8 passed, 1 skipped)

### T-002: Pytest configuration and fixture builders
- **Status:** PASS
- **Verification result:** `python3 -m pytest tests/unit -q` → 8 passed, 1 skipped; `python3 -m pytest -m csf_data -q` → 1 skipped
- **Acceptance criteria met:**
  - [x] Unit suite passes including `test_manifest_schema.py`, `test_mirage_split.py`
  - [x] `csf_data` tests skip without `MIRAGE_ABLATION_DATA_ROOT`

### T-003: Shared infrastructure — paths, subjects, provenance, hash gate
- **Status:** PASS
- **Verification result:** `test_paths.py`, `test_provenance.py` green; `python3 scripts/preflight.py` → PASS (unchanged message)
- **Acceptance criteria met:**
  - [x] `make_run_id` patterns (date-prefixed)
  - [x] Hash gate sidecar + registry checks in `verify_manifest_hashes()`
  - [x] `RunRecord` pydantic model + `write_run_record`
  - [x] Preflight output unchanged on laptop

### T-004: Fetch behavioural responses
- **Status:** PASS
- **Verification result:** CSF 2026-10-28 — all eight `~/scratch/.../ppdata/subj{01..08}/behav/responses.tsv` present; sync not required.
- **Acceptance criteria met:**
  - [x] 8× `responses.tsv` on scratch
  - [x] Sync logged in `runs/execution_log.md`

### T-004b: v3 beta re-sync (optional parallel)
- **Status:** PARTIAL (smoke submitted)
- **Verification result:** Slurm **`23913251`** — `SUBJ=01`, `BETA_VERSION=betas_fithrf_GLMdenoise_RR`. Session counts / dryrun parity pending job completion.
- **Acceptance criteria met:**
  - [ ] Session HDF5 counts / dryrun parity
  - [ ] Job IDs in registry + execution log

### T-005: Data-format probe on CSF
- **Status:** PARTIAL
- **Verification result:** `mirage_ablation/ingest/probe.py`, `ingest/cli.py --probe`, `s1_probe.sbatch`; unit tests `test_probe.py` green on synthetic fixtures.
- **Acceptance criteria met (real data):**
  - [ ] `format_probe.json` on scratch with all T-005 criteria (requires CSF sbatch after T-001 CSF env + data)

### T-050: CSF pytest jobscript
- **Status:** PARTIAL
- **Verification result:** `scripts/csf/pytest_track_b.sbatch` added. **Not submitted** (SSH blocked).
- **Acceptance criteria met:**
  - [ ] Unit suite passes on CSF at same commit

---

## Milestone Record

| Milestone | Status | Date | Notes |
|---|---|---|---|
| IP-1 Foundation | **COMPLETE (CSF)** | 2026-10-28 | Env **23914135**; pytest **23914147**; probe **23915227** PASS |

---

## Amendment 2026-10-28 (CSF resume)

**Git:** `f995320` on CSF home (bootstrap fix pushed from laptop).

**Root cause (job 23912772):** `/opt/apps/etc/modulefiles/interpreters/miniforge/README` — shared `miniforge` withdrawn 2026-10-26; `module load miniforge` fails on login and serial nodes.

**Fix:** Installed Miniforge3 to `~/miniforge3`; Slurm scripts source `scripts/csf/csf_conda_bootstrap.sh`.

**Slurm (submit from scratch, dependency chain):**

| Job ID | Script | Notes |
|--------|--------|-------|
| 23913250 | `create_track_b_env.sbatch` | T-001 CSF env + freeze |
| 23913397 | `pytest_track_b.sbatch` | `afterok:23913250` |
| 23913398 | `s1_probe.sbatch` | `afterok:23913250`, `BETA_VERSION=betas_fithrf` |
| 23913251 | `sync_m1_perception_subj.sbatch` | Optional T-004b smoke subj01 v3 |

**Monitor:** `sacct -j 23913250,23913397,23913398,23913251 -X --format=JobID,JobName,State,ExitCode,Elapsed`

**After 23913250 COMPLETED:** If `configs/environments/track_b.lock` changed on CSF repo clone inside job, `git pull` on laptop and commit lock. Verify probe output under `$SCRATCH/runs/*/format_probe.json`.

---

## Amendment 2026-10-28 (env retry — job 23913250 FAILED)

**Git:** CSF home pulled **`af29202`** (CPU-only IP-1 env install; GPU stack gated by `INSTALL_GPU=1`).

**Root cause (23913250):** `pip install -r requirements-track-b-gpu.txt` used wrong git repo for `pytorch-tools` (`pidgy/…` vs MIRAGE `pabloppp/…`).

**Slurm actions (execute-implementation-plan CSF handoff):**

| Job ID | Script | State / notes |
|--------|--------|----------------|
| 23913250 | `create_track_b_env.sbatch` | **FAILED** 1:0 (~5:32) |
| 23913397 | `pytest_track_b.sbatch` | **CANCELLED** (orphaned `afterok:23913250`) |
| 23913398 | `s1_probe.sbatch` | **CANCELLED** (orphaned `afterok:23913250`) |
| **23914049** | `create_track_b_env.sbatch` | **RUNNING** — no `INSTALL_GPU` |
| 23913251 | `sync_m1_perception_subj.sbatch` | **RUNNING** — v3 smoke subj01 (note only) |

**Monitor:** `sacct -j 23914049,23913251 -X --format=JobID,JobName,State,ExitCode,Elapsed`

**Pending (after 23914049 COMPLETED):** Resubmit `pytest_track_b.sbatch` and `s1_probe.sbatch` with `BETA_VERSION=betas_fithrf`; **do not** use `afterok` unless chaining fresh job IDs. Log IDs in registry + this log.

**Handoff:** IP-2 **not** started.

---

## Amendment 2026-10-28 (pyarrow pin — job 23914049 FAILED → 23914089)

**Git:** CSF home pulled **`9383632`** (`pyarrow>=14,<18` in `requirements-track-b.txt`; force reinstall in `create_track_b_env.sbatch`).

**Root cause (23914049):** Import probe — `pyarrow` 26 incompatible with pinned `numpy<2` (needs NumPy 2.0). Job **FAILED** 1:0 (~1:20).

**Slurm actions:**

| Job ID | Script | State / notes |
|--------|--------|----------------|
| 23914049 | `create_track_b_env.sbatch` | **FAILED** 1:0 — pyarrow/numpy mismatch |
| **23914089** | `create_track_b_env.sbatch` | **FAILED** 1:0 (~1:30) — force-reinstall → numpy 2.x / h5py |

**Monitor:** `sacct -j 23914089,23913251 -X --format=JobID,JobName,State,ExitCode,Elapsed`

**Pending (after 23914089 COMPLETED):** Resubmit `pytest_track_b.sbatch` and `s1_probe.sbatch` with `BETA_VERSION=betas_fithrf`; no `afterok`. Log IDs in registry + this log.

**Handoff:** IP-2 **not** started.

---

## Amendment 2026-10-28 (force-reinstall — job 23914089 FAILED → 23914135)

**Git:** CSF home pulled **`9295b81`** (`pyarrow==17.0.0`; install `numpy>=1.23.2,<2` before `-r requirements-track-b.txt`; removed force-reinstall from `create_track_b_env.sbatch`).

**Root cause (23914089):** `pip install --force-reinstall pyarrow` after main requirements upgraded **numpy to 2.4.6**; import probe failed on **h5py** (`numpy.dtype size changed`).

**Slurm actions:**

| Job ID | Script | State / notes |
|--------|--------|----------------|
| 23914089 | `create_track_b_env.sbatch` | **FAILED** 1:0 (~1:30) — force-reinstall → numpy 2.x / h5py |
| **23914135** | `create_track_b_env.sbatch` | **RUNNING** at handoff — no `INSTALL_GPU` |

**Monitor:** `sacct -j 23914135,23913251 -X --format=JobID,JobName,State,ExitCode,Elapsed`

**Pending (after 23914135 COMPLETED):** Resubmit `pytest_track_b.sbatch` and `s1_probe.sbatch` with `BETA_VERSION=betas_fithrf`; no `afterok`. Log IDs in registry + this log.

**Handoff:** IP-2 **not** started.

---

## Deviations Register

| # | Task | What Changed | Reason | Approved By |
|---|---|---|---|---|
| 1 | T-001 | Replaced `module load miniforge` with `scripts/csf/csf_conda_bootstrap.sh` + user `~/miniforge3` install on CSF | CSF removed shared miniforge module 2026-10-26 (README on module path); job 23912772 failed | User handoff 2026-10-28 (fix env bootstrap) |

---

## Open Issues

| # | Issue | Status | Resolution |
|---|---|---|---|
| 1 | CSF BatchMode SSH unavailable | Resolved | BatchMode OK 2026-10-28 |
| 2 | `track_b.lock` CPU-only from laptop venv | Resolved | CSF freeze copied 2026-10-28 (`89b00ee…`) |
| 3 | Probe/sbatch fixes not on `origin/main` | Open | Commit `probe.py` + `s1_probe.sbatch` + lock; CSF `git pull`; re-enable `git pull` in sbatch |

---

## CSF handoff commands (after Duo login)

```bash
ssh -Y csf3
cd ~/comp30030-mirage-ablation && git pull
cd ~/scratch/comp30030-mirage-ablation && sbatch ~/comp30030-mirage-ablation/scripts/csf/create_track_b_env.sbatch
# after env job OK:
bash ~/comp30030-mirage-ablation/scripts/csf/sync_m1_behav.sh
cd ~/scratch/comp30030-mirage-ablation && sbatch ~/comp30030-mirage-ablation/scripts/csf/pytest_track_b.sbatch
sbatch --export=ALL,BETA_VERSION=betas_fithrf ~/comp30030-mirage-ablation/scripts/csf/s1_probe.sbatch
# optional T-004b smoke:
sbatch --export=SUBJ=01,BETA_VERSION=betas_fithrf_GLMdenoise_RR ~/comp30030-mirage-ablation/scripts/csf/sync_m1_perception_subj.sbatch
```

Monitor: `sacct -j <JOBID> --format=JobID,State,ExitCode,Elapsed,MaxRSS`

---

**Handoff:** IP-2 **not** started.

---

## Amendment 2026-10-28 (IP-1 CSF verification — execute-implementation-plan)

**CSF git:** `52829fa` (AGENTS.md polling rules only; code at `9295b81` until probe/sbatch commit).

**Jobs (sequential handoff after env COMPLETED):**

| Job ID | Script | State | Notes |
|--------|--------|-------|-------|
| 23914135 | `create_track_b_env.sbatch` | **COMPLETED** 0:0 (~1:06) | T-001 CSF env |
| 23914147 | `pytest_track_b.sbatch` | **COMPLETED** 0:0 (~0:10) | 8 passed, 1 skipped |
| 23914156 | `s1_probe.sbatch` (serial) | **OUT_OF_MEMORY** 0:125 | `_nifti_info` loaded full 4D NIfTI |
| 23914541 | `s1_probe.sbatch` (serial) | **OUT_OF_MEMORY** 0:125 | same |
| 23914911 | `s1_probe.sbatch` (serial) | **OUT_OF_MEMORY** 0:125 | same |
| 23915059 | `s1_probe.sbatch` (`multicore_small -n 4`) | **FAILED** 1:0 | RAM OK; axis int16 + design count logic |
| **23915227** | `s1_probe.sbatch` (`multicore_small -n 4`) | **COMPLETED** 0:0 (~4:01) | `format_probe.json` **validation_pass: true** |

**Fixes (laptop, uncommitted — push before next CSF `git pull` in sbatch):**

- `mirage_ablation/ingest/probe.py`: skip 4D NIfTI full load (R13); int16 HDF5/NIfTI axis parity; design trial count = Σ `(dm rows × cols) // 60` over 12 `*_dm.mat` (720 = imagery betas rows).
- `scripts/csf/s1_probe.sbatch`: `-p multicore_small -n 4` (serial ~5 GB OOM on axis probe).

**Artifacts:** `runs/format_probe_subj01_betas_fithrf.json` (from scratch); `configs/environments/track_b.lock` synced from CSF (`89b00ee…`).

**T-005 criteria:** `voxel_order` [2,1,0]; `nsdgeneral` includes 1; imagery/design trials 720; all `.mat` readers recorded.

**Milestone IP-1:** exit criteria met on CSF; **IP-2 not started**. Recommend `post-implementation-review` after git commit of probe + sbatch + lock.

---

## Summary

- **Tasks completed:** T-002, T-003, T-004 PASS; T-001, T-005, T-050 PASS on CSF; T-004b PARTIAL (smoke job separate)
- **Milestone IP-1 exit criteria:** **MET** (env, pytest, `format_probe.json` all criteria)
- **Recommendation:** **COMPLETE (pending git commit/push of probe + s1_probe + lock)** — then `post-implementation-review`; do **not** start T-010+ until investigator commits
