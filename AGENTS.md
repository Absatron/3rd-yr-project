# Agent guide — COMP30030 mirage ablation

**Study slug:** `perception-imagery-latent-ablation`  
**Approved execution plan:** `docs/workflow_stages/execution_plans/2026-09-10-perception-imagery-latent-ablation-execution-plan.md`  
**Live status:** `docs/workflow_stages/execution_plans/2026-09-10-perception-imagery-latent-ablation-execution-log.md` · `runs/registry.yaml`  
**Implementation (S1–S4):** `implementation_plans/2026-10-27-perception-imagery-latent-ablation-s1-s4-ingest-implementation-plan.md` · decisions in `runs/registry.yaml` → `implementation_decisions`

## Living documentation (every agent turn)

When **any** of the following change — investigator decision (D1–D8), milestone, blocker, CSF job batch, or beta/data path — the **active agent** must update docs in the same session (before delegating to subagents that read them):

| Priority | File | Role |
|----------|------|------|
| 1 | `runs/registry.yaml` | Source of truth: decisions, job IDs, blockers, scratch paths |
| 2 | `runs/execution_log.md` | Dated narrative on the laptop/repo |
| 3 | `docs/workflow_stages/execution_plans/*-execution-log.md` | Study execution log (milestones, next tasks) |
| 4 | `docs/execution/data-and-compute-prerequisites.md` | S3 paths, beta version, tier sizes |
| 5 | `docs/CSF/csf-environment.md` | Slurm/sync commands aligned with registry |
| 6 | `scripts/csf/*.sbatch` | When sync targets or env vars change |

**Before** routing `execute-implementation-plan`, `execute-experiment`, or `reproducibility-investigator`: read `runs/registry.yaml` and confirm listed paths/decisions match the docs above.

**After** a large implementation milestone: optionally route **`documentation-reconciliation`** or **`provenance-reconciliation`** for a full sweep; that does not replace incremental updates at decision time.

**Do not** edit frozen upstream science (`hypothesis_formulation/`, `experimental_strategies/`, approved execution plan prose) to record operational choices — use registry + execution logs + implementation execution log instead.

## MIRAGE fidelity (all agents — read before changing code or data)

**Success criterion:** Track A **S12 gate** (MIRAGE notebooks, Setting A, `combined`) is the authoritative check that shared setup matches Kneeland et al. That gate comes **after** S1–S4, weights, and training — so **parity must be enforced during implementation**, not only at the end.

**Authority order for “what MIRAGE did”:**

1. Pinned **`MedARC-AI/MIRAGE`** at `registry.provenance.mirage_fork_commit` (once set) — especially `src/utils.py`, `Train.ipynb`, embedders  
2. **`docs/workflow_stages/model_designs/2026-09-06-perception-imagery-latent-ablation-option-3.md`** (dual-track contract)  
3. **`implementation_plans/2026-10-27-…-s1-s4-ingest-implementation-plan.md`** §3 research table (R1–R19) and **`runs/registry.yaml` → `implementation_decisions`**

**Rules:**

- **Track B (S1–S4):** Match MIRAGE numerics and trial logic where the plan cites R3/R4/R5 (betas v3, mask, ÷300, z-score rules, `load_nsd`-compatible matrices). **Physical paths** may differ (HDF5 per D3) if the **logical contract** and parity tests hold.  
- **Track A:** Notebook logic unchanged; only paths, env pins, manifest logging.  
- **Any deviation** from MIRAGE or from an recorded decision (D1–D8): **stop**, log in `implementation_plans/…-execution-log.md` and `runs/execution_log.md`, and either **justify** (investigator approval) or **reconcile** (update registry + living docs). Do not silently “improve” splits, beta version, normalisation, or embedder behaviour.  
- **Setting B** and ablation conditions are **intentional** divergences for hypothesis testing — never substitute them for Setting A gate inputs.

## Who should read what

**This file (`AGENTS.md`):** In Cursor, it is injected as a **workspace rule** for agents working in this repo (alongside `.cursor/rules/csf-remote-execution.mdc`). Subagents do not automatically load it unless the parent prompt or project rules include it — **parent turns must point executors at `AGENTS.md` + registry before CSF or ingest work.** Specialist skills (`execute-implementation-plan`, `execute-experiment`, etc.) list their own primary docs but still obey CSF and gating sections here when working on this project.

| Agent / skill | Primary docs |
|---------------|--------------|
| **execute-experiment** | Execution plan, execution log, `docs/execution/data-and-compute-prerequisites.md` |
| **execute-implementation-plan** | `implementation_plans/` (when present); same CSF rules below |
| **reproducibility-investigator** | Plan § leakage, manifest hashes, `runs/registry.yaml` |

## CSF3 remote execution (required for training/tests)

Heavy work runs on **CSF3 Slurm**, not the laptop. **`docs/CSF/ssh-access.md`** (SSH) · **`docs/CSF/csf-environment.md`** (miniforge, `aws`, `hf`, scratch).

| Item | Value |
|------|--------|
| SSH alias (Mac) | `csf3` → `csf3.itservices.manchester.ac.uk` |
| Username | `z29707aj` |
| Home repo | `~/comp30030-mirage-ablation` |
| Scratch (data/artifacts) | `~/scratch/comp30030-mirage-ablation` |
| Registry paths | `runs/registry.yaml` → `csf.*_absolute` |

### How agents run commands on CSF

1. **Prerequisite:** Investigator has an active SSH master session, or has logged in recently so **ControlMaster** is up (`ssh -O check csf3` → `Master running`). Login is **password + Duo**; agents cannot complete Duo without the user.
2. **From the Mac project environment**, use non-interactive remote commands:

   ```bash
   ssh -o BatchMode=yes csf3 'module load miniforge; export PATH=$HOME/.local/bin:$PATH; hostname; cd ~/comp30030-mirage-ablation && git pull'
   ```

3. **Never** store CSF/GitHub passwords in repo `.env` or commits.
4. **No compute on login nodes** — submit `sbatch` from `scripts/csf/` (see execution plan § CSF3).
5. After code changes: `git push` from laptop, then `git pull` on CSF home clone.

### Track A vs Track B on CSF

- **Track A (S12 gate):** MIRAGE notebooks / `scripts/track_a_gate.sh` — authoritative gate metrics.
- **Track B:** `mirage_ablation/` + `evaluation/` — blocked for **reporting** until Track A S12 PASS.
- **S0–S4** shared ingest runs once (Track B package); Track A consumes outputs under scratch `data/processed/`.

## Gating (do not skip)

- **M0 / HG-0:** Manifest frozen before training.
- **M1 (S1–S4):** Raw NSD on scratch must match **D1** in registry (`betas_fithrf_GLMdenoise_RR` for production). Legacy v2 `betas_fithrf` sync is complete but superseded — v3 re-sync is **implementation plan T-004b** (parallel with IP-1; required before production S1). Perception sync: `scripts/csf/sync_m1_perception_subj.sbatch` on **`serial`**, one `SUBJ` at a time (`docs/CSF/csf-environment.md`).
- **M2 / HG-2:** Track A S12 PASS before Track B ablation **reporting**.

See execution log **Active blockers** before starting GPU stages.

## Orchestration vs execution

The **chat agent orchestrates** (route specialists, update living docs, interpret failures). **`execute-implementation-plan`** and **`execute-experiment`** run CSF commands, code, and Slurm — the parent must **not** substitute for them on IP/experiment tasks. Parent prompts to those subagents must include: read **`AGENTS.md`** + **`runs/registry.yaml`**, and the **CSF job verification** rules below.

## CSF job verification (short jobs — do not submit-and-vanish)

**Problem:** Submitting `track_b_env`, pytest, or probe jobs and ending the turn immediately forces the investigator to discover `FAILED` in Slurm UI.

**Rule for `execute-implementation-plan` / `execute-experiment` on CSF:**

| Job class | Examples | Agent must |
|-----------|----------|------------|
| **Short** (typical ≤15 min on `serial`) | `create_track_b_env.sbatch`, `pytest_track_b.sbatch`, `s1_probe.sbatch`, behav sync | After `sbatch`, **poll** until `COMPLETED` or `FAILED` (e.g. `sacct` every 30–60s, use **Await** / repeated shell — budget **up to ~20 min** per job in one turn). On **FAILED**: `tail` the `#SBATCH -o` log, **fix repo if clear**, `git push`, CSF `git pull`, **resubmit** (same turn, up to **2 fix cycles** per job type). Only then hand off or chain the next sbatch. |
| **Long** (multi-hour) | M1 beta sync per subject, S1 production ingest, GPU training | Submit, log `job_id` + monitor command, **end turn** (no polling). |

On **COMPLETED** short jobs, run the **next dependent sbatch in the same turn** when IP-1 sequencing expects it (env → pytest → probe), unless blocked on investigator approval.

Log every job ID and outcome in `runs/execution_log.md` and the implementation execution log.

## Long jobs — hand off only when long

Do **not** keep an agent turn open for **multi-hour** work.

| Work | Agent pattern |
|------|----------------|
| Per-subject `aws s3 sync`, ridge, diffusion | Submit, log `job_id` + `sacct` command, **end turn** |
| Large HF bulk download | Batch job; do not poll until complete |

Investigator or a **new** turn checks `squeue` / `sacct` when long jobs finish.
