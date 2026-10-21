# Execution Artifacts Index

**Study:** Perception-to-Imagery Latent-Target Ablation (Option 3 — Dual-Track Hybrid)  
**Workflow step:** 4 — `execute-experiment`  
**Kickoff date:** 2026-09-10

This directory collects **operational execution documentation** (data prerequisites, compute planning, investigator checklists). Authoritative workflow artifacts remain under `docs/workflow_stages/`.

---

## Documents

| Document | Description |
| -------- | ----------- |
| [../CSF/ssh-access.md](../CSF/ssh-access.md) | CSF3 SSH, Duo, ControlMaster — **required for execute-experiment on cluster** |
| [../../AGENTS.md](../../AGENTS.md) | Agent index (executor SSH, paths, gates) |
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
| CSF3 bootstrap (miniforge, aws, hf) | **Ready** (2026-10-05) — `docs/CSF/csf-environment.md` |
| Agent SSH (ControlMaster) | `AGENTS.md` + `.cursor/rules/csf-remote-execution.mdc` |
| NSD DUA | **Confirmed** (investigator, 2026-10-21) |
| Scratch sync / M1 data on disk | **Not started** |
| M0 manifest freeze (HG-0) | **Not started** — no manifest JSON in repo yet |
| GPU training | **Not started** |
| `mirage_ablation/` / `track_a/` | Not vendored |

**Immediate next step:** Route **execute-experiment** — Slurm smoke, M0 metadata sync, scaffold + S0, then M1/HF selective download.

---

## Workflow context

See [scientific-workflow-overview.md](../workflows/scientific-workflow-overview.md) for the full dual-track pipeline. After execution completes, invoke `statistical-review` (Step 5).
