# Execution Log: Perception-to-Imagery Latent-Target Ablation

**Plan:** `2026-09-10-perception-imagery-latent-ablation-execution-plan.md`  
**Slug:** `perception-imagery-latent-ablation`  
**Model design:** Option 3 (dual-track hybrid)  
**Started:** 2026-09-10  
**Overall status:** **IN PROGRESS** — CSF + data-access ready; S0/M1 execution not started  
**Verdict:** N/A (no training yet)

---

## Summary

Kickoff (2026-09-10) created docs and registry. **2026-10-03–05:** CSF home/scratch layout, SSH multiplexing, miniforge, AWS CLI v2, Hugging Face login (`Absatron`), and `huggingface_hub<1.0` pin verified on CSF. **Investigator confirmed NSD Data Access Agreement submitted and approved** (2026-10-21). Scratch has no per-user quota; 3-month inactive-file cleanup applies.

**Not done yet:** `mirage_ablation/` + S0 scripts, manifest JSON population (M0), bulk NSD/HF sync to scratch (M1), Slurm smoke, Track A vendoring.

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
| ~~B3~~ | ~~HF/AWS path to data~~ | — | **Resolved 2026-10-05** — smoke on CSF; selective download not run to scratch yet |
| **B4** | `mirage_ablation/` + `scripts/s0_*` not implemented | Cannot run S0–S4 CLIs | **execute-experiment** next phase |
| ~~B5~~ | ~~CSF access~~ | — | **Resolved 2026-10-02** |
| ~~B6~~ | ~~CSF repo/scratch layout~~ | — | **Resolved 2026-10-03** |
| **B7** | M0 manifest files not on disk | HG-0 blocked | Run S0 after small metadata sync + scaffold |
| **B8** | `track_a/` + MIRAGE fork not vendored | Track A gate | Part of execute-experiment scaffold |
| **B9** | Slurm smoke not recorded | Ops confidence | `10-min_tutorial.md` + registry flag |

---

## Milestone tracker

| Milestone | Target stages | Status | Notes |
| --------- | ------------- | ------ | ----- |
| **M0** — Manifest frozen | S0 | **IN PROGRESS** | B4, B7 — JSON not created yet |
| **M1** — Data ready | S1–S4 | **NOT STARTED** | Scratch `data/raw` empty (~32K) |
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
| HG-0 — Manifest freeze | PENDING | — | After S0 population + review |
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
| 6 | Manifests frozen (M0 / HG-0) | **Not done** — only `manifests/README.md` exists |

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

### Kickoff — 2026-09-10

| Task | Result |
| ---- | ------ |
| K1–K3 scaffolding | **PASS** |
| K4–K6 package/GPU/HF bulk | **DEFERRED** |

---

## Next tasks (execute-experiment — ordered)

1. `git pull` on CSF; `git push` from laptop if docs commit pending.
2. Slurm smoke job → `csf.slurm_tutorial_complete: true`.
3. **M0 prep sync** to scratch: NSD/NSD-Imagery **metadata** + imagery betas (see prerequisites Tier / M0 table); dry-run first.
4. Implement `mirage_ablation/` minimal + `scripts/s0_populate_manifests.py` (or plan-equivalent).
5. Run **S0** → investigator **HG-0** sign-off in `runs/execution_log.md`.
6. **M1** perception betas sync (large; subject-at-a-time or Slurm) → S1–S4.
7. Selective HF weights to `scratch/.../data/frozen_weights/`.
8. Vendor `track_a/` + MIRAGE env → Track A TA.1+.

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
