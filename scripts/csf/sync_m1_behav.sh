#!/usr/bin/env bash
# Sync NSD behavioural responses.tsv for all subjects (small; login-node OK).
# Usage: DRYRUN=1 bash scripts/csf/sync_m1_behav.sh
set -euo pipefail

export PATH="${HOME}/.local/bin:${PATH}"
SCRATCH="${SCRATCH_ROOT:-${HOME}/scratch/comp30030-mirage-ablation}"
DRYRUN_FLAG=()
if [[ "${DRYRUN:-0}" == "1" ]]; then
  DRYRUN_FLAG=(--dryrun)
  echo "=== DRY RUN ==="
fi

for s in 01 02 03 04 05 06 07 08; do
  dest="${SCRATCH}/data/raw/nsd/ppdata/subj${s}/behav"
  mkdir -p "${dest}"
  aws s3 sync "${DRYRUN_FLAG[@]}" --no-sign-request \
    "s3://natural-scenes-dataset/nsddata/ppdata/subj${s}/behav/" \
    "${dest}/"
done

echo "M1 behav sync complete (DRYRUN=${DRYRUN:-0}) at $(date -Is)"
