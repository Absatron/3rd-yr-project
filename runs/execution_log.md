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
