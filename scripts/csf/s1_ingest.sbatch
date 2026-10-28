#!/bin/bash --login
# S1 production ingest (T-014 scaffold — submit only after T-004b + v3 format probe).
# sbatch -D ~/scratch/comp30030-mirage-ablation --export=ALL,BETA_VERSION=betas_fithrf_GLMdenoise_RR scripts/csf/s1_ingest.sbatch
# Smoke: override CLI args in smoke job or use laptop --sessions 1-2 → _smoke/

#SBATCH -p serial
#SBATCH -n 1
#SBATCH -a 1-8%4
#SBATCH -t 1-0
#SBATCH -o runs/slurm-logs/s1-%A_%a.out
#SBATCH -J mirage_s1

set -euo pipefail
export PATH="${HOME}/.local/bin:${PATH}"
# shellcheck disable=SC1091
source "${HOME}/comp30030-mirage-ablation/scripts/csf/csf_conda_bootstrap.sh"
SCRATCH="${SCRATCH_ROOT:-${HOME}/scratch/comp30030-mirage-ablation}"
REPO="${HOME}/comp30030-mirage-ablation"
ENV="${SCRATCH}/envs/track_b"
BETA_VERSION="${BETA_VERSION:-betas_fithrf_GLMdenoise_RR}"

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
  --manifest manifests/nsd_imagery_test_manifest_v1.json \
  --subject "${SLURM_ARRAY_TASK_ID}" \
  --beta-version "${BETA_VERSION}" \
  --overwrite
