#!/bin/bash --login
# CSF3 Slurm smoke test (docs/CSF/10-min_tutorial.md)
# Submit from scratch: sbatch ~/comp30030-mirage-ablation/scripts/csf/slurm_smoke.sbatch

#SBATCH -p serial
#SBATCH -t 5
#SBATCH -o slurm-%j.out
#SBATCH -J mirage_smoke

/bin/date
/bin/hostname
/bin/sleep 120
/bin/date
