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
