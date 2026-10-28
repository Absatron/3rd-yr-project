#!/bin/bash --login
# Run Track B pytest on CSF (T-050).
# Default: sbatch from ~/scratch/comp30030-mirage-ablation
# GPU: sbatch -p gpuL -G 1 -n 4 --export=ALL,PYTEST_ARGS="-m gpu -q" ...

#SBATCH -p serial
#SBATCH --ntasks=1
#SBATCH -t 1:00:00
#SBATCH -o runs/slurm-logs/pytest-%j.out
#SBATCH -J track_b_pytest

set -euo pipefail
module load miniforge
export PATH="${HOME}/.local/bin:${PATH}"
SCRATCH="${SCRATCH_ROOT:-${HOME}/scratch/comp30030-mirage-ablation}"
REPO="${HOME}/comp30030-mirage-ablation"
ENV="${SCRATCH}/envs/track_b"

export MIRAGE_ABLATION_DATA_ROOT="${SCRATCH}/data"
export MIRAGE_ABLATION_RUNS_ROOT="${SCRATCH}/runs"

mkdir -p "${SCRATCH}/runs/slurm-logs"
cd "${REPO}"
git pull
# shellcheck disable=SC1091
source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate "${ENV}"

python -m pytest ${PYTEST_ARGS:-tests/unit -q}
