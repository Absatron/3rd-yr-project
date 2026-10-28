#!/usr/bin/env bash
# Source conda for CSF Slurm jobs and interactive sessions.
# CSF withdrew general miniforge module access (2026-10-26); use ~/miniforge3.
# Usage: source scripts/csf/csf_conda_bootstrap.sh

_csf_conda_bootstrap() {
  if [[ -n "${CSF_CONDA_BOOTSTRAPPED:-}" ]]; then
    return 0
  fi
  if [[ -f "${HOME}/miniforge3/etc/profile.d/conda.sh" ]]; then
    # shellcheck disable=SC1091
    source "${HOME}/miniforge3/etc/profile.d/conda.sh"
    export CSF_CONDA_BOOTSTRAPPED=1
    return 0
  fi
  if module load miniforge 2>/dev/null; then
    export CSF_CONDA_BOOTSTRAPPED=1
    return 0
  fi
  if module load miniforge/24.11.2 2>/dev/null; then
    export CSF_CONDA_BOOTSTRAPPED=1
    return 0
  fi
  echo "ERROR: conda unavailable. Install Miniforge3 to ~/miniforge3 (see docs/CSF/csf-environment.md)." >&2
  return 1
}

_csf_conda_bootstrap
