# Execution Log: Perception-to-Imagery Latent-Target Ablation

**Plan:** `2026-09-10-perception-imagery-latent-ablation-execution-plan.md`  
**Slug:** `perception-imagery-latent-ablation`  
**Model design:** Option 3 (dual-track hybrid)  
**Started:** 2026-09-10  
**Overall status:** **IN PROGRESS** — S0 manifests populated; M0 scratch sync running on CSF; HG-0 pending  
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
| **B7** | HG-0 investigator sign-off pending | Training blocked | Review manifests + overlap audit; run `compare_mirage_training_split.py --write-audit` |
| **B8** | `track_a/` + MIRAGE fork not vendored | Track A gate | Deferred post-M1 |
| ~~B9~~ | ~~Slurm smoke not recorded~~ | — | **Resolved 2026-10-21** — job `23495544` |
| **B10** | M0 scratch sync in progress | M1 imagery ingest | Monitor `runs/m0_sync_2026-10-21.log` on CSF |
| **B11** | CLIP semantic audit `pending_weights` | S0.2 incomplete | After selective HF job `23495715` |

---

## Milestone tracker

| Milestone | Target stages | Status | Notes |
| --------- | ------------- | ------ | ----- |
| **M0** — Manifest frozen | S0 | **IN PROGRESS** | JSON + SHA256 in repo; **HG-0 unsigned** |
| **M1** — Data ready | S1–S4 | **IN PROGRESS** | M0 sync running; perception betas not started |
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
| HG-0 — Manifest freeze | PENDING | — | Manifests populated 2026-10-21 — **awaiting investigator review** |
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

### Kickoff — 2026-09-10

| Task | Result |
| ---- | ------ |
| K1–K3 scaffolding | **PASS** |
| K4–K6 package/GPU/HF bulk | **DEFERRED** |

---

## Next tasks (execute-experiment — ordered)

1. Confirm M0 sync complete on CSF (`du` imagery betas ≈12 GB).
2. **Investigator HG-0** — review `manifests/*.json` + overlap audit; sign `runs/execution_log.md`.
3. Re-run S0.2 audit after HF selective sync completes; refresh hashes if needed.
4. Submit M1 perception beta jobs: `sbatch --export=SUBJ=01 scripts/csf/sync_m1_perception_subj.sbatch` (×8).
5. Implement S1–S4 ingest CLIs; HG-1 after S4.
6. Vendor `track_a/` + MIRAGE env → Track A TA.1+ (still blocked until M1).

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
