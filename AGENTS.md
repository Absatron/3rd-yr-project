# Agent guide — COMP30030 mirage ablation

**Study slug:** `perception-imagery-latent-ablation`  
**Approved execution plan:** `docs/workflow_stages/execution_plans/2026-09-10-perception-imagery-latent-ablation-execution-plan.md`  
**Live status:** `docs/workflow_stages/execution_plans/2026-09-10-perception-imagery-latent-ablation-execution-log.md` · `runs/registry.yaml`

## Who should read what

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
- **M1 (S1–S4):** NSD + NSD-Imagery on scratch before ridge or Track A training. Perception beta S3 sync: `scripts/csf/sync_m1_perception_subj.sbatch` on **`serial`**, one `SUBJ` at a time (`docs/CSF/csf-environment.md`).
- **M2 / HG-2:** Track A S12 PASS before Track B ablation **reporting**.

See execution log **Active blockers** before starting GPU stages.

## Long jobs — submit and hand off (token-efficient)

Do **not** keep an agent turn open while waiting on multi-hour work.

| Work | Agent pattern |
|------|----------------|
| `sbatch` (ridge, GPU, sync) | Submit, log `job_id` + `sacct` check command in execution log, **end turn** |
| Large `aws s3 sync` | Prefer `scripts/csf/*.sbatch`; avoid foreground sync in chat |
| HF bulk download | Batch job or bounded smoke; do not poll until complete |

Investigator or a **new** turn checks `squeue` / `sacct` / scratch `du` when jobs finish. Cluster jobs run without an open SSH session.
