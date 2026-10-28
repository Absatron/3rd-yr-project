# Post-Implementation Review: M1 S1–S4 IP-1 Foundation

**Date:** 2026-10-28  
**Reviewer:** AI-assisted (post-implementation-review subagent)  
**Scope:** Milestone **IP-1 Foundation only** (T-001, T-002, T-003, T-004, T-005, T-050; T-004b scripts/smoke out of IP-1 exit scope)  
**Problem definition equivalent:** `docs/workflow_stages/pipeline_definitions/2026-09-06-perception-imagery-latent-ablation-pipeline-definition.md`  
**Solution design:** `docs/workflow_stages/model_designs/2026-09-06-perception-imagery-latent-ablation-option-3.md` (Track B package; MIRAGE fidelity applies to probe/read path semantics only at this milestone)  
**Implementation plan:** `implementation_plans/2026-10-27-perception-imagery-latent-ablation-s1-s4-ingest-implementation-plan.md`  
**Execution report:** `implementation_plans/2026-10-27-perception-imagery-latent-ablation-s1-s4-ingest-execution-log.md`  
**Git reviewed through:** `aedb41b` (registry marks IP-1 complete at implementation commit `3a09787`)

---

## 1. Review Scope & Method

- **Implementation version:** Commits `85764f7` (initial IP-1 code) through `aedb41b`, with primary CSF verification artifact commit `3a09787`.
- **Artifacts examined:** `mirage_ablation/config/paths.py`, `mirage_ablation/config/subjects.py`, `mirage_ablation/provenance.py`, `mirage_ablation/ingest/probe.py`, `mirage_ablation/ingest/cli.py`, `scripts/csf/*` (env, bootstrap, probe, pytest, behav sync, T-004b-related sync scripts), `tests/` (unit + integration marker), `configs/environments/track_b.lock`, `runs/format_probe_subj01_betas_fithrf.json`, `runs/registry.yaml` (`ip1_*`, `environment_pins`, `implementation_decisions`), `AGENTS.md` (CSF job verification), `docs/CSF/csf-environment.md`, `requirements-track-b.txt`, `scripts/preflight.py` (hash gate delegation).
- **Comparison approach:** Plan task acceptance criteria vs execution log claims vs on-disk code and committed JSON/YAML; deviations classified recorded vs unrecorded; MIRAGE-relevant probe behaviour traced to R3/R13/R14 in the plan.

---

## 2. Summary of Findings

| Category | Count |
|---|---|
| Recorded deviations (execution log Deviations Register + amendments) | 6 operative (1 formal register row + 5 amendment-only operational changes) |
| Unrecorded deviations (found in this review) | 8 |
| Emergent developments | 7 |
| Documentation gaps | 6 |

---

## 3. Plan vs Execution Report

| Planned item | Execution outcome | Recorded in log? | Notes |
|---|---|---|---|
| **T-001** Track B env + lock | **Different / PASS on CSF** | Partially | Laptop venv + lock early; CSF env job **23914135** COMPLETED after retries. Bootstrap uses `csf_conda_bootstrap.sh`, not plan’s `module load miniforge`. GPU stack deferred via `INSTALL_GPU=1` (not in original plan text). |
| **T-002** pytest.ini + conftest | **As planned / PASS** | Yes | 8 unit tests + integration marker; strict markers. |
| **T-003** paths, subjects, provenance, hash gate | **As planned / PASS** | Yes | `verify_manifest_hashes` in package; preflight delegates. |
| **T-004** behav sync script + 8× `responses.tsv` | **As planned / PASS** | Yes | Files pre-existing on scratch; script present. |
| **T-004b** v3 re-sync (optional parallel) | **Partial / Not done** | Yes | Smoke job **23913251** submitted; registry still notes RUNNING at handoff; no session-count/dryrun acceptance logged. |
| **T-005** format probe on CSF | **Different / PASS** | Yes (amendments) | Job **23915227** on `multicore_small -n 4`; `validation_pass: true` in repo JSON. Plan assumed `-p serial`; plan cited **576** imagery trials (R2); probe validates **720**. |
| **T-050** CSF pytest sbatch | **As planned / PASS** | Yes | Job **23914147**: 8 passed, 1 skipped. |

**Execution log internal inconsistency:** Header still says “CSF verification pending” and early task rows say T-001/T-005/T-050 PARTIAL, while the Milestone Record and final amendment state **IP-1 COMPLETE (CSF)**. Treat final amendment + `aedb41b` registry as authoritative; header/early rows are stale.

---

## 4. Execution Report vs Actual Implementation

| Area | Expected (per plan/report) | Actual implementation | Recorded? |
|---|---|---|---|
| CSF conda bootstrap | `module load miniforge` in sbatch (T-001, plan §6) | `scripts/csf/csf_conda_bootstrap.sh` → `~/miniforge3`; fallback `module load miniforge` | Yes (Deviation #1) |
| `track_b.lock` | CSF freeze copied to repo | `configs/environments/track_b.lock` at CSF freeze (`numpy==1.26.4`, `pyarrow==17.0.0`, `scipy==1.17.1`, …) | Yes |
| `requirements-track-b.txt` | Plan list (no `huggingface_hub`; `pyarrow` unpinned) | Adds `pyarrow==17.0.0`, `huggingface_hub>=0.26,<1.0` | No (unrecorded) |
| Env create sbatch | pip `-r requirements` only | Explicit `pip install "numpy>=1.23.2,<2"` before requirements; `INSTALL_GPU` optional GPU install | Yes (amendments) |
| `s1_probe.sbatch` partition | `-p serial` (T-005) | `-p multicore_small -n 4` | Yes (amendments) |
| Format probe beta version | D1 = v3 for production (registry) | Committed artifact uses **`betas_fithrf` (v2)** on scratch | Yes (artifact + registry `ip1_format_probe.beta_version`) |
| Imagery trial count check | Plan: match design; “expected 576” (R2) | HDF5 and design sum **720**; `imagery_trial_count_match: true` | Partially (720 noted; 576 plan mismatch not in Deviations Register) |
| `.mat` structure recording | “each `*_dm.mat`” reader recorded (T-005) | `_design_trial_count` reads **12** `*_dm.mat`; JSON `mat_files` lists **5** sample `*_dm` plus expdesign/design/pair lists only | No (unrecorded partial coverage) |
| 4D NIfTI in probe | Plan (b): shape of `betas_session01.nii.gz` | Shape recorded; uniques skipped with R13 note | Yes (artifact) |
| Axis HDF5↔NIfTI | Exact equality, 10 trials | `voxel_order` [2,1,0]; int16 uses `array_equal` without ÷300; float path uses ÷300 | Yes (code + amendment) |
| IP-1 CLI scope | Plan T-013 full S1 CLI later | `ingest/cli.py` implements **probe only**; non-probe exits 2 | Expected for IP-1 (not a deviation) |
| Registry IP-1 status | Executor T-051 later | `s1_s4_implementation_plan_status: ip1_foundation_complete`, `ip1_git_commit: "3a09787"` | Yes (`aedb41b`) |
| T-004b scripts | Parametrise perception sync; imagery v3 sync | `sync_m1_perception_subj.sbatch` has `BETA_VERSION`; `sync_m1_imagery_betas.sh` added | Yes (code); completion not logged |

---

## 5. Unrecorded Deviations (Critical)

| Deviation | Impact | Why it matters | Recommended action |
|---|---|---|---|
| Plan §5.3 / T-005 cite **576** imagery trials; data and probe use **720** | **High for IP-2** | T-011 acceptance and `imagery.h5` row count in plan assume 576; real betas file is 720 rows (12 runs × design-derived betas). Wrong row semantics break trial-table mapping and MIRAGE imagery parity. | Reconcile pipeline/plan §5.3 `T_img` and T-011 acceptance with probe formula; route to `reproducibility-investigator` if 576 vs 720 cognitive-trial definition is unclear. |
| `mat_files` in probe JSON does not enumerate all 12 `*_dm.mat` | Medium | T-005 acceptance: reader recorded for every design `.mat`; only subset appears in artifact (validation still passes). | Extend probe output or document that structure probe is sample-only while `_design_trial_count` is authoritative. |
| `huggingface_hub` in CPU requirements | Low | Not in T-001 plan list; bloats IP-1 env (needed later for S3). | Document in plan/env section or justify as forward dependency. |
| Unpinned `scipy` → **1.17.1** on CSF lock | Low–medium | Plan cites MIRAGE pins indirectly; large scipy jump vs laptop may diverge `loadmat` edge cases. | Pin scipy in requirements or record intentional float in registry `environment_pins`. |
| `requirements-track-b.txt` header still says `module load miniforge` | Low | Contradicts `csf-environment.md` and bootstrap script. | Update comment via documentation-reconciliation. |
| `tests/unit/test_probe.py` synthetic fixture still uses **576** | Low | Unit tests do not exercise `_design_trial_count` or 720-row real contract. | Add unit test for design trial sum helper; align synthetic counts with reconciled `T_img`. |
| Registry `ip1_csf_jobs.v3_resync_smoke_subj01.state_note: RUNNING` | Medium | Stale vs long-running smoke job; obscures T-004b readiness. | Update registry when job completes/fails. |
| Execution log title/status vs milestone table | Low | Readers may think IP-1 incomplete. | Reconcile execution log header and T-001/T-005/T-050 rows to final PASS state. |

---

## 6. Emergent Developments

| Development | Trigger | Current state | Should be documented as |
|---|---|---|---|
| User Miniforge at `~/miniforge3` + `csf_conda_bootstrap.sh` | CSF withdrew shared miniforge 2026-10-26 | Documented in `docs/CSF/csf-environment.md`; all Slurm scripts source bootstrap | **Accepted behaviour** (operational prerequisite) |
| `INSTALL_GPU=0` default for IP-1 env job | GPU pip failure (wrong `pytorch-tools` git URL) | CPU-only env sufficient for IP-1; GPU install gated | **Accepted behaviour** until IP-4 |
| NumPy/pyArrow pin chain (`pyarrow==17.0.0`, numpy 1.x first) | pyarrow 26 / force-reinstall broke h5py | Stable import probe on CSF | **Accepted behaviour**; record pins in plan T-001 |
| `multicore_small -n 4` for probe | Serial OOM on axis permutation (4D NIfTI slices) | Default in `s1_probe.sbatch` | **Accepted behaviour**; update plan T-005 / R18 RAM note |
| Int16 exact-match axis probe branch | Failed job 23915059 (dtype/scaling) | Aligns with raw int16 storage before ÷300 in S1 reader | **Accepted behaviour** for MIRAGE scaling contract |
| Design trial count = Σ `(dm rows × cols) // 60` over 12 runs | Imagery beta rows 720 ≠ 576 | Encoded in `probe.py`; passes validation | **Follow-up work**: reconcile with plan R2 text before T-011 |
| Skip heavy uniques on 4D beta NIfTI | R13 / OOM | Recorded in JSON with note | **Accepted behaviour** |

---

## 7. MIRAGE Fidelity Implications (Probe-Only Scope)

| Topic | MIRAGE / plan expectation | Implemented probe behaviour | Risk for Track A/B |
|---|---|---|---|
| Beta scaling (R3, R10) | int16 ÷300 for analysis | Axis check uses **raw int16 equality** between HDF5 and NIfTI; float path uses ÷300 | **Low** for axis discovery; S1 reader must still ÷300 (T-012 as planned) |
| Mask (R3) | `nsdgeneral == 1` | Records unique values `{-1,0,1}` including **1** | **Low** |
| HDF5 axis order (R13) | Must match masked reader | `voxel_order: [2,1,0]` from 10-trial exact match | **High if wrong** — current probe mitigates; value must flow to T-012 `flat_index` |
| Imagery trial inventory (R2) | Paper/manifest often describe **576** trial events | Betas HDF5 **720** rows; probe matches design-matrix-derived count | **High for IP-2** — T-011 must map 720 beta rows to run blocks/stimuli; do not assume 576-row `imagery.h5` from plan §5.3 without reconciliation |
| Beta version (D1, R1) | Production v3 `betas_fithrf_GLMdenoise_RR` | IP-1 probe artifact on **v2** `betas_fithrf` | **High for production S1** — not an IP-1 exit blocker; **required** re-probe on v3 after T-004b before trusting v3 layouts |
| NIfTI parity load (R13) | Avoid full 4D load | `dataobj` slices for axis probe; metadata-only for 4D uniques | **Low** — matches plan intent |

---

## 8. CSF Operational Deviations (Summary)

| Plan assumption | Actual | Logged? |
|---|---|---|
| `module load miniforge` | `~/miniforge3` + bootstrap script | Yes |
| Single env create success | Jobs 23913250, 23914049, 23914089 failed; fixed in `af29202`, `9383632`, `9295b81` | Yes (amendments + registry `ip1_csf_jobs`) |
| Full GPU stack in T-001 job | CPU-only unless `INSTALL_GPU=1` | Yes |
| Probe on `serial` | `multicore_small -n 4` after OOM | Yes |
| Short-job polling (AGENTS.md) | Multiple fix/resubmit cycles logged through **23915227** | Yes (`52829fa` codifies rule post-hoc) |

---

## 9. T-004b Status (Out of IP-1 Exit, In Scope for Review)

| Criterion (plan T-004b) | Status at `aedb41b` |
|---|---|
| Parametrised `sync_m1_perception_subj.sbatch` | **Done** (`BETA_VERSION`, conditional exclude) |
| Imagery v3 sync helper | **Done** (`sync_m1_imagery_betas.sh`) |
| Per-subject v3 trees on scratch | **Not verified** (smoke job 23913251 not closed out in registry) |
| Session HDF5 counts / dryrun parity | **Not logged** |
| Job IDs in registry `data_access.m1_perception_sync` | **Partial** (smoke entry only; stale RUNNING note) |

**Disposition:** T-004b remains **IP-2 / M1 gate** work before **T-014** production S1, not a reason to reject IP-1 foundation code.

---

## 10. Validation Enablement Review

N/A — research pipeline (per plan §13).

---

## 11. Documentation Reconciliation Actions

| Document | Change needed | Reason |
|---|---|---|
| `implementation_plans/2026-10-27-…-s1-s4-ingest-implementation-plan.md` §5.3, T-005, T-011 | Set authoritative **`T_img = 720`** (or split “576 events vs 720 GLM betas” if both are correct) and align acceptance bullets | Probe artifact and HDF5 contradict “576” text |
| Same plan, T-001 | Document `csf_conda_bootstrap.sh`, `INSTALL_GPU`, `pyarrow==17.0.0`, numpy-first install, optional `huggingface_hub` | Matches implemented CSF path |
| Same plan, T-005 | Default probe partition `multicore_small -n 4` with serial OOM note; optional full `*_dm.mat` listing in JSON | Matches `s1_probe.sbatch` and partial `mat_files` |
| `implementation_plans/…-execution-log.md` | Set **Date completed**, mark T-001/T-005/T-050 PASS; resolve “Open Issues” #3 (probe push) as closed at `3a09787` | Remove contradictory “pending” header |
| `runs/registry.yaml` → `ip1_csf_jobs.v3_resync_smoke_subj01` | Final `state`, `exit_code`, elapsed; link to `data_access.m1_perception_sync` when done | Stale RUNNING blocks operational truth |
| `requirements-track-b.txt` comment line | Replace “module load miniforge” with bootstrap doc pointer | Consistency with CSF docs |
| `docs/execution/data-and-compute-prerequisites.md` (if still v2-only wording) | Cross-link D1 v3 re-sync + IP-1 probe used v2 smoke | Avoid investigator assuming v3 probed |
| `AGENTS.md` | No change required for IP-1 content | CSF verification section matches executed retry/poll pattern |

Recommend routing to **`documentation-reconciliation`** with this review path; no upstream frozen science edits.

---

## 12. Risks Introduced by Deviations

| Risk | Source | Likelihood | Impact | Mitigation |
|---|---|---|---|---|
| Wrong imagery row count in T-011/T-013 | 576 vs 720 plan drift | Medium | High | Reconcile plan; use probe `design_matrix_trials` in T-011 specs |
| v3 layout differs from v2 probe | Probe only on `betas_fithrf` | Medium | High | Re-run probe with D1 `BETA_VERSION` after T-004b per subject |
| scipy unpinned drift | CSF lock 1.17.1 | Low | Medium | Pin or document |
| Stale T-004b registry blocks scheduling | RUNNING note | Medium | Low | Update registry on job completion |
| Incomplete `.mat` audit trail | Sample `mat_files` list | Low | Medium | Extend probe or document scope |

---

## 13. Suitability for Future Changes

- **Is the current documentation sufficient for safe modification?** **No** — imagery trial count (576 vs 720), T-004b completion state, and execution log header must be reconciled before IP-2 trial builders are treated as spec-complete.
- **Missing for a new engineer/agent:** Single authoritative `T_img` definition; closed-out v3 smoke/resync jobs; explicit note that GPU env is not yet installed on CSF.
- **New design/plan required?** **No** — amendments to implementation plan §5.3 and T-005/T-011 suffice unless reproducibility review finds 720 is incorrect.

---

## 14. Final Assessment

| Question | Answer |
|---|---|
| Implementation matches documented reality (code vs execution log final amendment) | **Mostly yes** at `3a09787`/`aedb41b`; execution log header/early rows **no** |
| All deviations recorded | **No** — see §5 |
| Documentation fit for IP-2 code work | **Conditional yes** after reconciliation of **720-row imagery contract** |
| IP-1 plan exit criteria (env locked; unit green laptop+CSF; format_probe all criteria) | **Met** at committed artifact (`validation_pass: true`, pytest job PASS, env job PASS) |

### Verdict: Acceptable to start IP-2?

**Yes — start IP-2 implementation tasks (T-010–T-013 code, laptop unit tests, CSF smoke with existing v2 data)** provided investigators treat the following as **active gates**, not IP-1 regressions:

**Blockers before T-014 (production S1 ingest), not before starting T-010:**

1. **T-004b** complete for all subjects (D1 v3 on scratch) with session counts and dryrun parity logged in registry + execution logs.  
2. **Format probe re-run** on at least subj01 (and preferably all subjects if layouts differ) with **`betas_fithrf_GLMdenoise_RR`**, committed JSON or registry pointers updated.  
3. **Plan/pipeline reconciliation** of imagery beta row count (**720** vs documented **576**) so T-011/T-013 acceptance criteria are unambiguous.

**Non-blocking follow-ups:** close v3 smoke job status in registry; extend probe `mat_files` coverage or document sampling; pin/document scipy; refresh execution log top matter.

### Required Follow-Up Actions

1. Invoke **`documentation-reconciliation`** using this file’s §11 table.  
2. Before T-014, invoke **`execute-implementation-plan`** (or investigator) to finish **T-004b** and v3 format probe.  
3. If 720 vs 576 is not explained by NSD-Imagery docs alone, invoke **`reproducibility-investigator`** before locking T-011 mapping logic.

---

## 15. Task-by-Task Planned vs Actual (IP-1)

| Task | Planned | Actual (`aedb41b`) | Status |
|---|---|---|---|
| T-001 | Conda env on scratch, lock, laptop venv | CSF **23914135**; bootstrap + CPU stack + pins; laptop OK | **PASS** (GPU half deferred) |
| T-002 | pytest.ini, conftest, markers | Present; 8 unit tests | **PASS** |
| T-003 | paths, subjects, provenance, hash gate | Implemented + tests | **PASS** |
| T-004 | behav sync + 8 files | Script + files on scratch | **PASS** |
| T-004b | Optional v3 resync | Scripts + smoke submitted; acceptance open | **PARTIAL** (outside IP-1 exit) |
| T-005 | probe.py, cli probe, sbatch, criteria | PASS on v2; operational fixes | **PASS** (with documented deltas) |
| T-050 | pytest sbatch | **23914147** PASS | **PASS** |
