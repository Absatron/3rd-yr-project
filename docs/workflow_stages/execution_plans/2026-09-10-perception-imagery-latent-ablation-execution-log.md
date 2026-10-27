# Execution Log: Perception-to-Imagery Latent-Target Ablation

**Plan:** `2026-09-10-perception-imagery-latent-ablation-execution-plan.md`  
**Slug:** `perception-imagery-latent-ablation`  
**Model design:** Option 3 (dual-track hybrid)  
**Started:** 2026-09-10  
**Overall status:** **IN PROGRESS** — HG-0 signed; M0 complete; M1 **`serial`** — subj01–03 **COMPLETE**; subj04 **partial** (job `23828368` FAILED, S3 timeout); retry 04 then 05–08  
**Verdict:** N/A (no training yet)

---

## Summary

Kickoff (2026-09-10) created docs and registry. **2026-10-03–05:** CSF home/scratch layout, SSH multiplexing, miniforge, AWS CLI v2, Hugging Face login (`Absatron`), and `huggingface_hub<1.0` pin verified on CSF. **Investigator confirmed NSD Data Access Agreement submitted and approved** (2026-10-21). Scratch has no per-user quota; 3-month inactive-file cleanup applies.

**2026-10-21 (execute-experiment):** `mirage_ablation/` S0 scaffold + manifest JSON committed (`d9e745d`); Slurm smoke **PASS** (job `23495544`); M0 `sync_m0_metadata.sh` dry-run + real sync **in progress** on scratch; selective HF download submitted (job `23495715`). **HG-0 not signed.** Track A vendoring still open.

---

## Plan approval

| Field | Value |
| ----- | ----- |
| Plan document | `docs/workflow_stages/execution_plans/2026-09-10-perception-imagery-latent-ablation-execution-plan.md` |
| Approved | 2026-09-10 |
| Approved by | Investigator |
| Git commit at kickoff | `c9e89c2b65553c77c5f89330a84e664a04be8c1a` |

---

## Active blockers

| ID | Blocker | Impact | Resolution |
| -- | ------- | ------ | ---------- |
| ~~B1~~ | ~~NSD Data Access form~~ | — | **Resolved** — investigator confirmed submitted/approved; manual received |
| ~~B2~~ | ~~NSD-Imagery access~~ | — | **Resolved** — same DUA; paths in prerequisites doc |
| ~~B3~~ | ~~HF/AWS path to data~~ | — | **Resolved 2026-10-05** — smoke on CSF |
| ~~B4~~ | ~~`mirage_ablation/` + `scripts/s0_*`~~ | — | **Resolved 2026-10-21** — S0 scaffold committed |
| ~~B5~~ | ~~CSF access~~ | — | **Resolved 2026-10-02** |
| ~~B6~~ | ~~CSF repo/scratch layout~~ | — | **Resolved 2026-10-03** |
| ~~B7~~ | ~~HG-0 investigator sign-off~~ | — | **Resolved 2026-10-22** — manifest `1.0.0` frozen |
| **B8** | `track_a/` + MIRAGE fork not vendored | Track A gate (M2) | Deferred post-M1 perception sync |
| ~~B9~~ | ~~Slurm smoke not recorded~~ | — | **Resolved 2026-10-21** — job `23495544` |
| ~~B10~~ | ~~M0 scratch sync in progress~~ | — | **Resolved 2026-10-21** — log `2026-10-21T16:15:38+01:00`; ~12G `data/raw` |
| **B11** | CLIP semantic audit `pending_weights` | S0.2 incomplete | HF selective job delivered captions only; no `*clip*` paths on `reesekneeland/MIRAGE` dataset — need CLIP source per plan |
| **B12** | S1–S4 ingest CLIs not implemented | M1 ingest blocked | `mirage_ablation/ingest/` stub only — route `execute-implementation-plan` |

---

## Milestone tracker

| Milestone | Target stages | Status | Notes |
| --------- | ------------- | ------ | ----- |
| **M0** — Manifest frozen | S0 | **COMPLETE** | HG-0 signed 2026-10-22; SHA256 in registry |
| **M1** — Data ready | S1–S4 | **IN PROGRESS** | subj01–03 perception betas on scratch (`23630151`, `23824802`, `23827408`); subj04–08 manual **serial** sync; S1–S4 **DEFERRED** (no CLIs) |
| **M2** — Track A gate pass | TA.1–TA.5 | **BLOCKED** | Needs M0, M1, B8 |
| M3 — Track B ridges fit | S5–S6 | NOT STARTED | — |
| M4 — Latent cache complete | S7 | NOT STARTED | — |
| M5 — Decoder metrics | S8 | BLOCKED | Requires M2 for reporting |
| M6 — Reconstructions | S9–S10 | NOT STARTED | — |
| M7 — Parity confirmed | parity | NOT STARTED | — |
| M8 — Primary inference | S11 Setting A | NOT STARTED | — |
| M9 — Secondary inference | S11 Setting B | NOT STARTED | — |
| M10 — Repro bundle | export | NOT STARTED | — |

---

## Human checkpoint gates

| Gate | Status | Signed | Notes |
| ---- | ------ | ------ | ----- |
| HG-0 — Manifest freeze | **SIGNED** | 2026-10-22 | Investigator; manifest `1.0.0` |
| HG-1 — Leakage checklist | PENDING | — | After S4 |
| HG-2 — Track A S12 gate | PENDING | — | After M2 |
| HG-3 — Parity audit | PENDING | — | — |
| HG-4 — Setting B branch | PENDING | — | — |
| HG-5 — Manuscript stats | PENDING | — | — |

---

## Infrastructure checklist (investigator + CSF) — 2026-10-21

| # | Item | Status |
| - | ---- | ------ |
| 1 | NSD DUA submitted/approved | **Done** (investigator) |
| 2 | CSF SSH + agent multiplex | **Done** — `AGENTS.md` |
| 3 | HF CLI logged in on CSF | **Done** — `hf auth whoami` → Absatron |
| 4 | AWS `s3 ls` NSD bucket `--no-sign-request` on CSF | **Done** |
| 5 | Scratch space adequate | **Done** — shared Lustre; fair use; 3-month cleanup |
| 6 | Manifests populated (M0 / HG-0) | **Populated** — freeze after HG-0 sign-off |
| 7 | Slurm smoke | **Done** — `23495544` |

---

## Task log

### CSF bootstrap — 2026-10-05 (investigator terminal)

| Task | Result |
| ---- | ------ |
| `module load miniforge` → Python 3.12.8 | **PASS** |
| `huggingface_hub` 2.2.0 download | **FAIL** (httpx2 bug) |
| Downgrade `huggingface_hub>=0.26,<1.0` | **PASS** |
| `hf auth login` + smoke download `.gitattributes` | **PASS** |
| AWS CLI v2 user install + `s3 ls` NSD | **PASS** |
| Scratch layout present, empty data | **PASS** |

### Execute-experiment — M0/S0 scaffold — 2026-10-21

| Task | Result |
| ---- | ------ |
| CSF `git pull` @ `d9e745d` | **PASS** |
| Slurm smoke `scripts/csf/slurm_smoke.sbatch` | **PASS** — job `23495544`, exit `0:0` |
| M0 `DRYRUN=1 sync_m0_metadata.sh` on CSF | **PASS** |
| M0 real sync (background) | **IN PROGRESS** — log `~/scratch/.../runs/m0_sync_2026-10-21.log` |
| S0 manifest population (official `cue_pair_list.xlsx`) | **PASS** — 18 stimuli; hashes in repo |
| Overlap audit (Setting A exact COCO) | **PASS** vs MIRAGE mask — subj 2/5/7 `exact_seen` matches `load_nsd`; doc + `compare_mirage_training_split.py` |
| Selective HF download | **SUBMITTED** — Slurm `23495715` |
| HG-0 sign-off | **NOT DONE** (by design) |

**M1 plan (next):** After M0 sync completes, submit `sync_m1_perception_subj.sbatch` with `SUBJ=01`…`08` sequentially (~45–65 GB/subject); then S1 ingest CLIs.

### Execute-experiment — M1 kickoff — 2026-10-22

| Task | Result |
| ---- | ------ |
| CSF `git pull` (`d9e745d` → `ec39711`) | **PASS** |
| M0 verify: log end `2026-10-21T16:15:38+01:00`; `data/raw` ≈12G | **PASS** |
| M0 verify: `nsd_stim_info_merged.csv`, `cue_pair_list.xlsx` on scratch | **PASS** |
| M0 verify: imagery betas subj01–08 (~1.3–1.7G/subj) | **PASS** |
| HF selective job `23495715` (`sacct`) | **UNKNOWN** — SlurmDB `Connection refused` on login node |
| HF artifacts on scratch | **PARTIAL** — captions `.npy` only; no CLIP weights (HF dataset has no `*clip*` paths) |
| S0.2 CLIP audit re-run | **SKIPPED** — weights absent (B11) |
| M1 `sbatch` subj01 (plain) | **FAIL** — multicore requires ≥2 CPUs |
| M1 `sbatch --cpus-per-task=2 --export=SUBJ=01` | **SUBMITTED** — job `23630151`, partition `multicore`, node `node1229` |
| S1–S4 ingest | **DEFERRED** — no ingest CLIs in repo (B12) |

**Monitor M1 subj01:**

```bash
ssh -o BatchMode=yes csf3 'squeue -u z29707aj; tail -f ~/comp30030-mirage-ablation/slurm-m1-subj-23630151.out'
ssh -o BatchMode=yes csf3 'sacct -j 23630151 --format=JobID,State,ExitCode,Elapsed -X'
du -sh ~/scratch/comp30030-mirage-ablation/data/raw/nsd/betas/subj01
```

**After subj01 COMPLETED:** submit `SUBJ=02` … `08` (one at a time). Repo `sync_m1_perception_subj.sbatch` patched with `#SBATCH --cpus-per-task=2` (push + `git pull` on CSF).

### Execute-experiment — M1 continuation — 2026-10-26

| Task | Result |
| ---- | ------ |
| CSF `git pull` (`ec39711` → `498738a`) | **PASS** (miniforge module absent on login node; pull succeeded) |
| Verify subj01 on scratch | **PASS** — `du -sh` **61G**; `sacct -j 23630151` **COMPLETED** `0:0`, elapsed **00:07:20** |
| Verify subj02–08 on scratch | **PASS** — no perception beta dirs (only subj01 present) |
| M1 `sbatch --export=SUBJ=02` (script includes `--cpus-per-task=2`) | **SUBMITTED** — job `23816141`, partition `multicore`, state **PENDING** (Reason=Priority; Slurm est. `StartTime=2026-11-02 03:15`) |
| M1 subj03–08 | **NOT STARTED** — waiting for subj02 **COMPLETED** per plan |

**Monitor M1 subj02:**

```bash
ssh -o BatchMode=yes csf3 'squeue -j 23816141'
ssh -o BatchMode=yes csf3 'sacct -j 23816141 --format=JobID,State,ExitCode,Elapsed -X'
ssh -o BatchMode=yes csf3 'tail -20 ~/comp30030-mirage-ablation/slurm-m1-subj-23816141.out'
ssh -o BatchMode=yes csf3 'du -sh ~/scratch/comp30030-mirage-ablation/data/raw/nsd/betas/subj02'
```

**When subj02 COMPLETED (~45–65G):** submit `SUBJ=03` … `08` sequentially (one sbatch at a time).

### Execute-experiment — M1 serial partition — 2026-10-26

| Task | Result |
| ---- | ------ |
| Diagnose multicore queue | subj02 job `23816141` **PENDING (Priority)** ~2h+; `scontrol` est. start ~4 days; not a script error |
| Test subj03 on multicore | Job `23824709` also **PENDING (Priority)** — same queue behaviour |
| Cancel multicore jobs | `scancel 23816141`, `scancel 23824709` |
| M1 subj02 on **`serial`** | **SUBMITTED** job `23824802` — **RUNNING** immediately (`node921`) |
| Repo default partition | `sync_m1_perception_subj.sbatch` → `#SBATCH -p serial`, 1 CPU (docs updated) |

**Policy:** All remaining M1 perception syncs use **`serial`** only. Use **`multicore`** later for S1–S2 ingest / parallel CPU, not for `aws s3 sync`.

### Execute-experiment — M1 subj02 complete, subj03 started — 2026-10-26 (evening)

| Task | Result |
| ---- | ------ |
| CSF `git pull` | `498738a` → `d98f7db` (serial sbatch default + docs) |
| subj02 job `23824802` | **COMPLETED** `0:0`, `00:45:48`, scratch **62G** |
| subj03 on **`serial`** | **COMPLETED** job `23827408` (`0:0`, ~23 min); scratch **~50G** |
| Duplicate subj03 job `23826369` | Overlap with agent submit — **`scancel`** if still queued/running |
| Laptop → CSF SSH | **BLOCKED** ~18:23 UTC — DNS resolution failure; cluster jobs unaffected |

**Remaining:** Submit `SUBJ=04` … `08` sequentially on **`serial`** (investigator manual chain).

### M1 subj04 failed — 2026-10-26 / follow-up 2026-10-27

| Item | Detail |
| ---- | ------ |
| Job `23828368` | **FAILED** `1:0`, ~31 min; scratch **36G** (expect ~45–65G) |
| Cause | `AWS_IO_SOCKET_TIMEOUT` on CSF compute node → S3 (not laptop VPN) |
| Action | Re-`sbatch --export=SUBJ=04`; `sync_m1_perception_subj.sbatch` updated with retry passes |

### Kickoff — 2026-09-10

| Task | Result |
| ---- | ------ |
| K1–K3 scaffolding | **PASS** |
| K4–K6 package/GPU/HF bulk | **DEFERRED** |

---

## Next tasks (execute-experiment — ordered)

1. **Investigator:** M1 `SUBJ=04`…`08` via **`serial`** sbatch (one at a time). subj01–03 done (`23630151`, `23824802`, `23827408`). `scancel 23826369` if duplicate still active.
2. Resolve B11 — define CLIP checkpoint source (not on `reesekneeland/MIRAGE` HF dataset); then `s0_populate_manifests.py --audit` + `compare_mirage_training_split.py --write-audit`.
3. Route **execute-implementation-plan** for S1–S4 ingest CLIs (B12); HG-1 after S4.
4. Vendor `track_a/` + MIRAGE env (B8) after M1 perception betas on scratch for train subjects.
5. Do **not** start Track A GPU until M1 perception sync complete for required subjects.

---

## Readiness: route to execute-experiment? — 2026-10-21

| Question | Answer |
| -------- | ------ |
| Infrastructure + legal access ready? | **Yes** |
| Manifests ready without S0? | **No** — item 6 is **not** satisfied |
| Track A training now? | **No** — needs M0, M1, scaffolding |
| **Start execute-experiment for data + S0 + scaffold?** | **Yes** |

**Verdict:** Clear to **route execute-experiment** for Slurm smoke, scratch sync (M0-sized then M1), package scaffold, and S0 manifest population — **not** for Track A GPU gate until M0/HG-0 and M1 progress.

---

## Tracker run IDs

No experiment runs logged yet.

---

## Recommendations

- Keep `ssh -Y csf3` master open when agents run remote commands.
- Do not put HF tokens in repo `.env`; CSF token is in `~/.cache/huggingface/` on cluster home.
- After M6+: `statistical-review`. Leakage concerns: `reproducibility-investigator`.
