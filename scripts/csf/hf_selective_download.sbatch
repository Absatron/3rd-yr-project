#!/bin/bash --login
# Selective HF weights/captions to scratch (login-style I/O; no GPU)

#SBATCH -p serial
#SBATCH -t 12:00:00
#SBATCH -o slurm-hf-%j.out
#SBATCH -J mirage_hf_sel

set -euo pipefail
module load miniforge
export PATH="${HOME}/.local/bin:${PATH}"
REPO="${HOME}/comp30030-mirage-ablation"
SCRATCH="${HOME}/scratch/comp30030-mirage-ablation"
export MIRAGE_ABLATION_DATA_ROOT="${SCRATCH}/data"

cd "${REPO}"
python -m pip install --user -q "huggingface_hub>=0.26,<1.0"
python scripts/csf/hf_selective_download.py --dest "${SCRATCH}/data/frozen_weights/mirage_hf"
