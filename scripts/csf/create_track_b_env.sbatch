#!/bin/bash --login
# Create Track B conda env on scratch and freeze packages (T-001).
# Submit from scratch: sbatch ~/comp30030-mirage-ablation/scripts/csf/create_track_b_env.sbatch
# After job: copy configs/environments/track_b.lock from freeze output and commit.

#SBATCH -p serial
#SBATCH --ntasks=1
#SBATCH -t 4:00:00
#SBATCH -o runs/slurm-logs/create-track-b-env-%j.out
#SBATCH -J track_b_env

set -euo pipefail
export PATH="${HOME}/.local/bin:${PATH}"
# shellcheck disable=SC1091
source "${HOME}/comp30030-mirage-ablation/scripts/csf/csf_conda_bootstrap.sh"
SCRATCH="${SCRATCH_ROOT:-${HOME}/scratch/comp30030-mirage-ablation}"
REPO="${HOME}/comp30030-mirage-ablation"
ENV="${SCRATCH}/envs/track_b"

mkdir -p "${SCRATCH}/runs/slurm-logs" "${SCRATCH}/runs/env"
cd "${REPO}"
git pull

if [[ ! -d "${ENV}" ]]; then
  conda create -y -p "${ENV}" python=3.11
fi
# shellcheck disable=SC1091
source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate "${ENV}"

python --version
pip install --upgrade pip
pip install -r "${REPO}/requirements-track-b.txt"
pip install --force-reinstall "pyarrow>=14.0.0,<18.0.0"
# IP-1 (S1–S4 ingest/probe): CPU stack only. GPU deps for S3 (IP-4): sbatch --export=INSTALL_GPU=1 ...
if [[ "${INSTALL_GPU:-0}" == "1" ]]; then
  pip install -r "${REPO}/requirements-track-b-gpu.txt"
fi

pip freeze > "${SCRATCH}/runs/env/track_b.freeze.txt"
cp "${SCRATCH}/runs/env/track_b.freeze.txt" "${REPO}/configs/environments/track_b.lock"

python -c "import h5py, scipy.io, nibabel, pandas, pyarrow, pydantic, openpyxl; print('import_probe_ok')"
python --version

echo "Track B env ready at ${ENV} $(date -Is)"
