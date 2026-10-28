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
| IP-1 Foundation | **IN PROGRESS** | 2026-10-28 | CSF jobs submitted; await env/pytest/probe completion |

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

## Deviations Register

| # | Task | What Changed | Reason | Approved By |
|---|---|---|---|---|
| 1 | T-001 | Replaced `module load miniforge` with `scripts/csf/csf_conda_bootstrap.sh` + user `~/miniforge3` install on CSF | CSF removed shared miniforge module 2026-10-26 (README on module path); job 23912772 failed | User handoff 2026-10-28 (fix env bootstrap) |

---

## Open Issues

| # | Issue | Status | Resolution |
|---|---|---|---|
| 1 | CSF BatchMode SSH unavailable | Resolved | BatchMode OK 2026-10-28 |
| 2 | `track_b.lock` CPU-only from laptop venv | Open | Re-copy after job **23913250** COMPLETED |
| 3 | miniforge module missing on serial | Resolved | `f995320` bootstrap + `~/miniforge3` |

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

## Summary

- **Tasks completed:** 3 PASS (T-002, T-003, T-004), 4 PARTIAL (T-001, T-004b, T-005, T-050), 0 FAIL
- **Milestone IP-1 exit criteria:** NOT fully met (await jobs 23913250 → 23913397/23913398)
- **Recommendation:** **INCOMPLETE** — verify sacct + probe JSON; commit lock if freeze differs; then `post-implementation-review`
- **Next:** `post-implementation-review` after IP-1 exit criteria satisfied; do **not** start T-010+ until probe PASS
