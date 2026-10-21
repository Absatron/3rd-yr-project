#!/usr/bin/env bash
# M0 metadata + NSD-Imagery imagery betas → scratch (dry-run if DRYRUN=1)
set -euo pipefail

export PATH="${HOME}/.local/bin:${PATH}"
SCRATCH="${SCRATCH_ROOT:-${HOME}/scratch/comp30030-mirage-ablation}"
DRYRUN_FLAG=()
if [[ "${DRYRUN:-0}" == "1" ]]; then
  DRYRUN_FLAG=(--dryrun)
  echo "=== DRY RUN ==="
fi

mkdir -p "${SCRATCH}/data/raw/nsd/experiments/nsd"
mkdir -p "${SCRATCH}/data/raw/nsd_imagery/experiments/nsdimagery"
mkdir -p "${SCRATCH}/runs/slurm-logs"

aws s3 sync "${DRYRUN_FLAG[@]}" --no-sign-request \
  s3://natural-scenes-dataset/nsddata/experiments/nsd/ \
  "${SCRATCH}/data/raw/nsd/experiments/nsd/"

aws s3 sync "${DRYRUN_FLAG[@]}" --no-sign-request \
  s3://natural-scenes-dataset/nsddata/experiments/nsdimagery/ \
  "${SCRATCH}/data/raw/nsd_imagery/experiments/nsdimagery/"

for s in 01 02 03 04 05 06 07 08; do
  mkdir -p "${SCRATCH}/data/raw/nsd/ppdata/subj${s}/func1pt8mm/roi"
  aws s3 sync "${DRYRUN_FLAG[@]}" --no-sign-request \
    "s3://natural-scenes-dataset/nsddata/ppdata/subj${s}/func1pt8mm/roi/" \
    "${SCRATCH}/data/raw/nsd/ppdata/subj${s}/func1pt8mm/roi/"
done

for s in 01 02 03 04 05 06 07 08; do
  dest="${SCRATCH}/data/raw/nsd_imagery/betas/subj${s}/func1pt8mm/nsdimagerybetas_fithrf"
  mkdir -p "${dest}"
  aws s3 sync "${DRYRUN_FLAG[@]}" --no-sign-request \
    "s3://natural-scenes-dataset/nsddata_betas/ppdata/subj${s}/func1pt8mm/nsdimagerybetas_fithrf/" \
    "${dest}/"
done

echo "M0 sync complete (DRYRUN=${DRYRUN:-0}) at $(date -Is)"
