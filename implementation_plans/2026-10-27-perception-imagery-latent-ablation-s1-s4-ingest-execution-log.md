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
- **Status:** PARTIAL
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
- **Status:** PARTIAL
- **Verification result:** `scripts/csf/sync_m1_behav.sh` added (DRYRUN=1 pattern). Sync **not executed** on CSF (SSH blocked).
- **Acceptance criteria met:**
  - [ ] 8× `responses.tsv` on scratch
  - [ ] Sync logged in `runs/execution_log.md` (pending CSF run)

### T-004b: v3 beta re-sync (optional parallel)
- **Status:** PARTIAL (scripts only)
- **Verification result:** `sync_m1_perception_subj.sbatch` parametrized with `BETA_VERSION`; `sync_m1_imagery_betas.sh` added. No v2 trees deleted. **No sbatch submitted** (SSH blocked).
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
| IP-1 Foundation | **BLOCKED** | 2026-10-28 | Laptop code/tests complete; CSF env, behav sync, probe, pytest blocked on SSH |

---

## Deviations Register

| # | Task | What Changed | Reason | Approved By |
|---|---|---|---|---|
| — | — | none | — | — |

---

## Open Issues

| # | Issue | Status | Resolution |
|---|---|---|---|
| 1 | CSF BatchMode SSH unavailable | Open | Investigator: `ssh -Y csf3`, then git pull on CSF, sbatch env → pytest → behav sync → s1_probe |
| 2 | `track_b.lock` CPU-only from laptop venv | Open | Re-copy from `$SCRATCH/runs/env/track_b.freeze.txt` after `create_track_b_env.sbatch` |

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

- **Tasks completed:** 2 PASS, 5 PARTIAL, 0 FAIL (CSF-dependent criteria open)
- **Milestone IP-1 exit criteria:** NOT fully met (`format_probe.json` + CSF unit suite pending)
- **Recommendation:** **INCOMPLETE** — complete CSF handoff, then re-verify IP-1 before IP-2
- **Next:** `post-implementation-review` after IP-1 exit criteria satisfied; do **not** start T-010+ until probe PASS
