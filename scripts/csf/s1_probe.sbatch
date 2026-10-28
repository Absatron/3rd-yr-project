#!/bin/bash --login
# S1 format probe on CSF scratch (T-005).
# sbatch --export=ALL,BETA_VERSION=betas_fithrf scripts/csf/s1_probe.sbatch
# v3 production: BETA_VERSION=betas_fithrf_GLMdenoise_RR after T-004b

#SBATCH -p serial
#SBATCH --ntasks=1
#SBATCH -t 2:00:00
#SBATCH -o runs/slurm-logs/s1-probe-%j.out
#SBATCH -J mirage_s1_probe

set -euo pipefail
export PATH="${HOME}/.local/bin:${PATH}"
# shellcheck disable=SC1091
source "${HOME}/comp30030-mirage-ablation/scripts/csf/csf_conda_bootstrap.sh"
SCRATCH="${SCRATCH_ROOT:-${HOME}/scratch/comp30030-mirage-ablation}"
REPO="${HOME}/comp30030-mirage-ablation"
ENV="${SCRATCH}/envs/track_b"
BETA_VERSION="${BETA_VERSION:-betas_fithrf}"

export MIRAGE_ABLATION_DATA_ROOT="${SCRATCH}/data"
export MIRAGE_ABLATION_RUNS_ROOT="${SCRATCH}/runs"

mkdir -p "${SCRATCH}/runs/slurm-logs"
cd "${SCRATCH}"
cd "${REPO}"
git pull
# shellcheck disable=SC1091
source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate "${ENV}"

python -m mirage_ablation.ingest.cli \
  --stage S1 \
  --probe \
  --subject 1 \
  --beta-version "${BETA_VERSION}" \
  --manifest manifests/nsd_imagery_test_manifest_v1.json \
  --overwrite
