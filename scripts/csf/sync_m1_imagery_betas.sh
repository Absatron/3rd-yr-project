#!/usr/bin/env bash
# Sync one subject's NSD-Imagery beta HDF5 (v3 default per D1).
# Usage: SUBJ=01 IMAGERY_BETA_VERSION=betas_fithrf_GLMdenoise_RR bash scripts/csf/sync_m1_imagery_betas.sh
set -euo pipefail

export PATH="${HOME}/.local/bin:${PATH}"
SCRATCH="${SCRATCH_ROOT:-${HOME}/scratch/comp30030-mirage-ablation}"
SUBJ="${SUBJ:?set SUBJ=01..08}"
BV="${IMAGERY_BETA_VERSION:-betas_fithrf_GLMdenoise_RR}"
IMAG_DIR="nsdimagery${BV}"

dest="${SCRATCH}/data/raw/nsd_imagery/betas/subj${SUBJ}/func1pt8mm/${IMAG_DIR}"
mkdir -p "${dest}"
aws s3 sync --no-sign-request \
  "s3://natural-scenes-dataset/nsddata_betas/ppdata/subj${SUBJ}/func1pt8mm/${IMAG_DIR}/" \
  "${dest}/"

echo "Imagery beta sync subj${SUBJ} ${IMAG_DIR} done $(date -Is)"
