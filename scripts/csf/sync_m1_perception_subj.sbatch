#!/bin/bash --login
# M1 Tier-3: sync one subject's NSD perception betas to scratch (large I/O).
# Usage: sbatch --export=SUBJ=01 sync_m1_perception_subj.sbatch

#SBATCH -p multicore
#SBATCH --cpus-per-task=2
#SBATCH -t 24:00:00
#SBATCH -o slurm-m1-subj-%j.out
#SBATCH -J mirage_m1_beta

set -euo pipefail
export PATH="${HOME}/.local/bin:${PATH}"
SCRATCH="${SCRATCH_ROOT:-${HOME}/scratch/comp30030-mirage-ablation}"
SUBJ="${SUBJ:?set SUBJ=01..08}"

DEST="${SCRATCH}/data/raw/nsd/betas/subj${SUBJ}"
mkdir -p "${DEST}"

aws s3 sync --no-sign-request \
  "s3://natural-scenes-dataset/nsddata_betas/ppdata/subj${SUBJ}/func1pt8mm/betas_fithrf/" \
  "${DEST}/func1pt8mm/betas_fithrf/" \
  --exclude "*func1mm*" \
  --exclude "*MNI*" \
  --exclude "*betas_assumehrf*" \
  --exclude "*betas_fithrf_GLMdenoise_RR*" \
  --exclude "*nsdimagery*" \
  --exclude "*nsdsynthetic*" \
  --exclude "*resting*"

echo "M1 perception beta sync subj${SUBJ} done $(date -Is)"
