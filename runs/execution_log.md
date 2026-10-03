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
