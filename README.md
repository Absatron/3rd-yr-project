# 3rd Year Project: Perception-to-Imagery Latent-Target Ablation

COMP30030 dissertation — MIRAGE-based ablation (image / text / combined latent targets) on NSD-Imagery.

- **Plan:** `docs/project-plan.md` · **Gantt CSV:** `docs/project-plan-gantt.csv`
- **Execution plan:** `docs/workflow_stages/execution_plans/2026-09-10-perception-imagery-latent-ablation-execution-plan.md`
- **CSF:** `docs/CSF/README.md`

Clone on CSF (home) — see `docs/CSF/ssh-access.md` for SSH/Duo and scratch layout:

```bash
git clone https://github.com/Absatron/3rd-yr-project.git ~/comp30030-mirage-ablation
mkdir -p ~/scratch/comp30030-mirage-ablation/{data/raw,data/processed,data/frozen_weights,artifacts,runs/slurm-logs}
```

Large NSD data lives on **scratch**, not in this repository.
