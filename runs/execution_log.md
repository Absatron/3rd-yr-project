# Execution Log (append-only narrative)

**Study:** perception-imagery-latent-ablation (Option 3 dual-track)  
**Registry:** `runs/registry.yaml`  
**Authoritative stage log:** `docs/workflow_stages/execution_plans/2026-09-10-perception-imagery-latent-ablation-execution-log.md`

---

## 2026-09-10 — Execute-experiment kickoff

**Event:** Step 4 (`execute-experiment`) initiated per approved execution plan (2026-09-10).

**Actions completed:**

- Created execution scaffolding: `runs/registry.yaml`, `manifests/README.md`, `docs/execution/`
- Documented data and compute prerequisites (`docs/execution/data-and-compute-prerequisites.md`)
- Recorded plan approval and current blockers in workflow execution log

**Explicitly not started (per kickoff scope):**

- GPU training or inference
- Full MIRAGE Hugging Face download (~300 GB)
- `mirage_ablation/` package implementation

**Blockers:**

1. NSD Data Access form not yet submitted/approved
2. NSD-Imagery access not yet confirmed
3. Selective Hugging Face artifact list not yet validated against on-disk layout

**Next investigator actions:**

1. Submit NSD and NSD-Imagery data access forms (see `docs/execution/data-and-compute-prerequisites.md` Phase 0)
2. After approval, run AWS sync dry-runs with official exclude patterns
3. Selective-download MIRAGE HF artifacts (weights, captions, precomputes only)

**Human gates:** None signed. HG-0 pending manifest population (blocked on data access + package scaffold).

---

## 2026-10-21 — CSF ready; NSD DUA confirmed; route execute-experiment

**Event:** Investigator confirmed NSD Data Access Agreement submitted and approved (manual received earlier). CSF bootstrap verified 2026-10-05: miniforge, `huggingface_hub<1.0`, HF login (Absatron), AWS CLI v2, NSD S3 `--no-sign-request`, empty scratch layout with ample shared pool.

**Blockers cleared:** B1, B2, B3 (access path); B5, B6 (CSF layout/SSH).

**Still open:** B4 package/S0 scripts; B7 manifest JSON not created; B8 Track A vendoring; B9 Slurm smoke; M1 scratch sync.

**Human gates:** HG-0 still **pending** — manifests are **not** ready until S0 runs.

**Next:** Invoke `execute-experiment` per ordered list in workflow execution log (Slurm smoke → M0 sync → scaffold → S0 → M1).

---

## 2026-10-21 — S0 scaffold, Slurm smoke, M0 sync started (CSF)

**Host:** CSF3 (`z29707aj`) via SSH BatchMode; repo `~/comp30030-mirage-ablation` @ `d9e745db6eda83348a2fbfbead30cdf9c00a0315`.

**Commands (representative):**

```bash
# Slurm smoke (scratch cwd)
cd ~/scratch/comp30030-mirage-ablation && sbatch ~/comp30030-mirage-ablation/scripts/csf/slurm_smoke.sbatch
# → job 23495544, COMPLETED 0:0, ~2 min

# M0 metadata + imagery betas
cd ~/comp30030-mirage-ablation && DRYRUN=1 bash scripts/csf/sync_m0_metadata.sh
nohup bash -c 'DRYRUN=0 bash scripts/csf/sync_m0_metadata.sh' \
  > ~/scratch/comp30030-mirage-ablation/runs/m0_sync_2026-10-21.log 2>&1 &

# S0 (scratch data root)
export MIRAGE_ABLATION_DATA_ROOT=~/scratch/comp30030-mirage-ablation/data
python scripts/s0_populate_manifests.py
python scripts/s0_populate_manifests.py --audit --threshold 0.85
python scripts/s0_verify_manifests.py --write-hashes

# Selective HF (not full 300GB bundle)
sbatch ~/comp30030-mirage-ablation/scripts/csf/hf_selective_download.sbatch
# → job 23495715
```

**Artifacts:** Manifests committed on `main` (`manifests/nsd_imagery_test_manifest_v1.json`, `stimulus_overlap_audit.json`, `.sha256` sidecars). Registry updated: `csf.slurm_tutorial_complete: true`, manifest SHA256 recorded; `manifest_frozen_at` still null.

**Human gates:** HG-0 **not signed** — review manifests and overlap audit; confirm `mirage_split_verification` via `python scripts/compare_mirage_training_split.py --write-audit` (non-zero `exact_seen` on subj 2/5/7 aligns with MIRAGE `load_nsd`, not a reproduction blocker).

**M1 plan:** When M0 log shows completion, run `sbatch --export=SUBJ=NN scripts/csf/sync_m1_perception_subj.sbatch` for `NN=01..08` (one subject at a time).

---

## 2026-10-22 — HG-0 manifest freeze signed

**Event:** Investigator reviewed and signed **HG-0** (manifest `1.0.0`, overlap audit with `mirage_split_verification.all_subjects_agree`).

**Recorded in:** `runs/registry.yaml` (`manifest_frozen_at: 2026-10-22`).

**Cleared:** B7 (HG-0). M0 sync confirmed complete on CSF (log ended 2026-10-21T16:15:38+01:00; ~12G `data/raw`).

**Next:** M1 — perception beta sync per subject via Slurm; then S1–S4 when ingest CLIs exist. B11 (CLIP semantic audit) remains non-blocking for M1 sync.

---

## 2026-10-26 — M1 sync: use `serial` partition

**Event:** `multicore` M1 jobs (`23816141`, `23824709`) stuck **PENDING (Priority)** with multi-day estimated start. **`serial`** job `23824802` (subj02) started immediately.

**Policy:** `scripts/csf/sync_m1_perception_subj.sbatch` defaults to **`serial`**; documented in `docs/CSF/csf-environment.md` and prerequisites. Remaining subjects **03–08** after subj02 completes.

**M1 chaining:** Background execute-experiment run for subj02–08 was **stopped by investigator** (2026-10-26); subj02 Slurm job `23824802` continues on CSF. Submit `SUBJ=03`…`08` manually after each **COMPLETED** (~45–65 min/subject on serial).

---

## 2026-10-22 — M1 perception sync started (CSF)

**Host:** CSF3 via SSH BatchMode; repo pulled to `ec39711`.

**M0 verification (scratch):** `m0_sync_2026-10-21.log` ended `2026-10-21T16:15:38+01:00`; `data/raw` ≈12G; `nsd_stim_info_merged.csv` and `cue_pair_list.xlsx` present; imagery betas for subj01–08 (~1.3–1.7G each).

**M1 submission:**

```bash
cd ~/comp30030-mirage-ablation
sbatch --cpus-per-task=2 --export=SUBJ=01 scripts/csf/sync_m1_perception_subj.sbatch
# → job 23630151 (RUNNING on multicore)
```

**HF selective (`23495715`):** Captions on scratch under `data/frozen_weights/mirage_hf/`; `sacct` unavailable (DB connection refused). No CLIP weight files — MIRAGE HF dataset has no `clip`-named artifacts (B11).

**S1–S4:** **DEFERRED** — ingest package stub only (B12).

**Monitor:** `squeue -u z29707aj`; `sacct -j 23630151 -X`; `slurm-m1-subj-23630151.out` in CSF home repo.

---

## 2026-10-26 — M1 perception sync continuation (CSF)

**Host:** CSF3 via SSH BatchMode; repo pulled `ec39711` → `498738a`.

**Verified:** subj01 perception betas **61G** on scratch; job `23630151` **COMPLETED** (`0:0`, 7m20s). subj02–08 dirs absent.

**Submitted:**

```bash
cd ~/comp30030-mirage-ablation
sbatch --export=SUBJ=02 scripts/csf/sync_m1_perception_subj.sbatch
# → job 23816141 (PENDING, Reason=Priority; Slurm est. start 2026-11-02 03:15)
```

**Remaining:** After subj02 completes, submit `SUBJ=03` … `08` sequentially.

**Monitor:** `squeue -j 23816141`; `sacct -j 23816141 -X`; `slurm-m1-subj-23816141.out`; `du -sh ~/scratch/.../betas/subj02`.

---

## 2026-10-26 — M1 perception sync serial chain (CSF)

**Host:** CSF3 via SSH BatchMode; repo pulled `498738a` → `d98f7db`.

**subj02 (job `23824802`):** **COMPLETED** `0:0`, elapsed `00:45:48`, ended `2026-10-26T17:10:08+00:00`. Scratch `betas/subj02` **62G**. Slurm log: `slurm-m1-subj-23824802.out`.

**subj03:** Investigator submit **COMPLETED** — job **`23827408`** (`0:0`, ~23 min, log `subj03 done` 18:04 UTC). Scratch **~50G**. Overlapping job **`23826369`** (background agent, 17:12) — **`scancel 23826369`** if still in `squeue`.

**Next:** `sbatch --export=SUBJ=04` … `08` on CSF after each **COMPLETED** (manual chain; background [M1 serial sync](b6ab2953-9e5d-4b13-b5d1-9b8c14af2d55) stopped by investigator).

---

## 2026-10-27 — M1 subj04 sync failed (retry)

**Job `23828368`:** **FAILED** `1:0` (~31 min). Log: `AWS_IO_SOCKET_TIMEOUT` on last ~30 files (~43 GiB transferred). Scratch **36G** (incomplete). Runs on CSF compute node — **not** caused by laptop VPN drop.

**Fix:** Re-submit `sbatch --export=SUBJ=04 …` (idempotent `aws s3 sync`). Repo: `sync_m1_perception_subj.sbatch` adds AWS adaptive retries + up to 3 sync passes.

---

## 2026-10-27 — M1 perception sync verified (all 8 subjects)

CSF scratch: `betas/subj01`–`subj08` present (~42–62G each). Local file counts match S3 for all subjects; subj03 has 62 extra local files (dual-sync overlap). **M1 download gate passed**; remaining M1 work is S1–S4 + HF weights on scratch.

---

## 2026-10-27 — subj03 perception betas reconciled to S3

**Cause:** overlapping serial sync jobs left ~62 extra local files under `betas_fithrf/`.  
**Fix:** `sync_m1_perception_subj.sbatch` now passes `aws s3 sync --delete`; re-ran `sbatch --export=SUBJ=03` (job **`23855894`**, COMPLETED ~20s). Post-check: `aws s3 sync --dryrun --delete` reports **0** deltas for subj03.

---

## 2026-10-27 — S1–S4 implementation plan drafted (B12)

**Artifact:** `implementation_plans/2026-10-27-perception-imagery-latent-ablation-s1-s4-ingest-implementation-plan.md` ([implementation-plan](17e4fcaf-b375-46c8-b156-20861d4f022b)).  
**Status:** Under review — investigator must approve plan and record **D1–D8** before **`execute-implementation-plan`**.  
**Note:** Scratch betas are v2 (`betas_fithrf`); plan default **D1** is v3 (`betas_fithrf_GLMdenoise_RR`) + conditional re-sync (T-004b).

**Investigator decisions (2026-10-27):** **D1** = v3 + re-sync all subjects; **D3** = HDF5 + parquet indexes; **D4** = audited exceptions for MIRAGE-aligned imagery training IDs. **Execute:** deferred until plan read-through — then **IP-1** (`execute-implementation-plan`).

---

## 2026-10-28 — IP-1 laptop complete; CSF handoff to execute-implementation-plan

**Commit:** `85764f7` ([execute-implementation-plan](6173327d-0719-4732-976f-47bf3ec52882)) — T-002/T-003 PASS on laptop; T-001/T-004/T-005/T-050 code ready.

**Orchestration:** Parent agent must **not** run CSF sbatch/sync on behalf of IP-1; route **`execute-implementation-plan`** for CSF verification only.

**CSF notes (2026-10-28):** BatchMode SSH available. `create_track_b_env.sbatch` job **`23912772`** FAILED (`module load miniforge` missing on node). Behav sync may have been started separately — executor to verify eight `responses.tsv` and fix env bootstrap per `docs/CSF/csf-environment.md` before pytest + `s1_probe`.

**CSF resume (2026-10-28 PM):** Commit **`f995320`** — `csf_conda_bootstrap.sh` + user **`~/miniforge3`**. T-004 **PASS** (8× `responses.tsv` on scratch). Slurm: env **`23913250`**, pytest **`23913397`** (`afterok:23913250`), probe **`23913398`** (`BETA_VERSION=betas_fithrf`), optional v3 smoke subj01 **`23913251`**. Monitor: `sacct -j 23913250,23913397,23913398,23913251 -X --format=JobID,State,ExitCode,Elapsed`.

**Exit IP-1 before IP-2:** CSF env + `format_probe.json` all T-005 criteria PASS.

---

## 2026-10-28 — IP-1 Foundation implementation (Track B ingest scaffold)

**Executor:** `execute-implementation-plan` milestone IP-1.  
**Log:** `implementation_plans/2026-10-27-perception-imagery-latent-ablation-s1-s4-ingest-execution-log.md`

**Laptop completed:** `requirements-track-b*.txt`, `pytest.ini`, `tests/conftest.py`, `mirage_ablation/config/{paths,subjects}.py`, `mirage_ablation/provenance.py`, ingest probe CLI, CSF jobscripts (`create_track_b_env`, `pytest_track_b`, `s1_probe`, `sync_m1_behav`, T-004b parametrized perception sync).  
**Tests:** `python3 -m pytest tests/unit -q` → 8 passed, 1 skipped (2026-10-28).

**CSF blocked:** BatchMode SSH denied (Duo). Pending: env sbatch, `sync_m1_behav.sh`, `pytest_track_b.sbatch`, `s1_probe.sbatch`, optional v3 subj01 sync. After login: `git pull` on `~/comp30030-mirage-ablation` then submit from `~/scratch/comp30030-mirage-ablation`.

**Registry:** `environment_pins.track_b_python` = 3.11.5; `v3_resync_status` = scripts_ready_awaiting_csf_submit.

---
