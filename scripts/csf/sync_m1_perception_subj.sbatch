#!/bin/bash --login
# M1 Tier-3: sync one subject's NSD perception betas to scratch (large I/O).
# Production path (D1): betas_fithrf_GLMdenoise_RR — parameterize via T-004b (implementation plan).
# Legacy script target: betas_fithrf (v2 on scratch until v3 re-sync).
# Usage: sbatch --export=SUBJ=01,BETA_VERSION=betas_fithrf_GLMdenoise_RR sync_m1_perception_subj.sbatch

# I/O-bound S3 sync; serial queue starts much faster than multicore on CSF3.
#SBATCH -p serial
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH -t 24:00:00
#SBATCH -o slurm-m1-subj-%j.out
#SBATCH -J mirage_m1_beta

set -euo pipefail
export PATH="${HOME}/.local/bin:${PATH}"
export AWS_MAX_ATTEMPTS="${AWS_MAX_ATTEMPTS:-15}"
export AWS_RETRY_MODE="${AWS_RETRY_MODE:-adaptive}"
SCRATCH="${SCRATCH_ROOT:-${HOME}/scratch/comp30030-mirage-ablation}"
SUBJ="${SUBJ:?set SUBJ=01..08}"
BETA_VERSION="${BETA_VERSION:-betas_fithrf_GLMdenoise_RR}"

DEST="${SCRATCH}/data/raw/nsd/betas/subj${SUBJ}"
mkdir -p "${DEST}"

S3_SRC="s3://natural-scenes-dataset/nsddata_betas/ppdata/subj${SUBJ}/func1pt8mm/${BETA_VERSION}/"
S3_DST="${DEST}/func1pt8mm/${BETA_VERSION}/"
SYNC_EXCLUDES=(
  --exclude "*func1mm*"
  --exclude "*MNI*"
  --exclude "*betas_assumehrf*"
  --exclude "*nsdimagery*"
  --exclude "*nsdsynthetic*"
  --exclude "*resting*"
)
if [[ "${BETA_VERSION}" == "betas_fithrf" ]]; then
  SYNC_EXCLUDES+=(--exclude "*betas_fithrf_GLMdenoise_RR*")
fi

# Transient AWS_IO_SOCKET_TIMEOUT on CSF→S3 is common near end of large syncs; re-run is idempotent.
max_passes=3
for pass in $(seq 1 "${max_passes}"); do
  echo "aws s3 sync pass ${pass}/${max_passes} subj${SUBJ} $(date -Is)"
  if aws s3 sync --delete --no-sign-request "${S3_SRC}" "${S3_DST}" "${SYNC_EXCLUDES[@]}"; then
    break
  fi
  if [[ "${pass}" -eq "${max_passes}" ]]; then
    echo "sync failed after ${max_passes} passes" >&2
    exit 1
  fi
  sleep 120
done

echo "M1 perception beta sync subj${SUBJ} done $(date -Is)"
