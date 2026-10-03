# Execution Artifacts Index

**Study:** Perception-to-Imagery Latent-Target Ablation (Option 3 — Dual-Track Hybrid)  
**Workflow step:** 4 — `execute-experiment`  
**Kickoff date:** 2026-09-10

This directory collects **operational execution documentation** (data prerequisites, compute planning, investigator checklists). Authoritative workflow artifacts remain under `docs/workflow_stages/`.

---

## Documents

| Document | Description |
| -------- | ----------- |
| [data-and-compute-prerequisites.md](./data-and-compute-prerequisites.md) | Two data sources (NSD S3 vs MIRAGE HF), milestone download checklist (M0–M2), compute table, dependency gates, investigator action list |
| [../workflow_stages/execution_plans/2026-09-10-perception-imagery-latent-ablation-execution-plan.md](../workflow_stages/execution_plans/2026-09-10-perception-imagery-latent-ablation-execution-plan.md) | Approved execution plan (scripts, stages, acceptance criteria) |
| [../workflow_stages/execution_plans/2026-09-10-perception-imagery-latent-ablation-execution-log.md](../workflow_stages/execution_plans/2026-09-10-perception-imagery-latent-ablation-execution-log.md) | Live execution log (task outcomes, blockers, gate sign-offs) |

---

## Repository paths (execution runtime)

| Path | Role |
| ---- | ---- |
| `runs/registry.yaml` | Study metadata, milestone status, manifest hashes, gate outcomes |
| `runs/execution_log.md` | Append-only investigator narrative |
| `runs/{run_id}/run.json` | Per-job structured log (created when jobs run) |
| `manifests/` | S0 frozen test manifest and audit files |
| `data/raw/` | NSD and NSD-Imagery after AWS sync |
| `data/frozen_weights/` | Selective MIRAGE HF checkpoints |
| `artifacts/` | Model outputs (ridge, latents, reconstructions, metrics) |
| `track_a/` | MIRAGE notebooks for S12 gate (not yet vendored) |
| `mirage_ablation/` | Track B package (deferred — blocked on data access) |

---

## Current status

| Item | Status |
| ---- | ------ |
| Execution plan | Approved 2026-09-10 |
| Data access (NSD / NSD-Imagery) | **Pending** |
| M0 manifest freeze | Blocked |
| GPU training | **Not started** (by design) |
| `mirage_ablation/` package | Deferred |

**Immediate next step:** Investigator completes data access forms and selective artifact planning per [data-and-compute-prerequisites.md](./data-and-compute-prerequisites.md).

---

## Workflow context

See [scientific-workflow-overview.md](../workflows/scientific-workflow-overview.md) for the full dual-track pipeline. After execution completes, invoke `statistical-review` (Step 5).
