# CSF3 environment bootstrap (z29707aj)

Reference for **manual setup** and **execute-experiment** agents. Verified on login nodes **2026-10-05** (see terminal log in project history).

Related: [ssh-access.md](./ssh-access.md) · [AGENTS.md](../../AGENTS.md) · scratch policy in [response.md](./response.md).

## Every interactive / agent SSH session on CSF

```bash
module load miniforge
export PATH="$HOME/.local/bin:$PATH"
cd ~/comp30030-mirage-ablation
```

Default login `python` is **3.9** until `miniforge` is loaded → **3.12.8**.

Optional — append to `~/.bashrc` on CSF (once):

```bash
module load miniforge
export PATH="$HOME/.local/bin:$PATH"
```

## Mac SSH (common mistake)

| Wrong | Right |
|-------|--------|
| `ssh -Y ~/.ssh/id_ed25519_csf3 user@host` | `ssh -Y csf3` (key in `~/.ssh/config`) |
| | or `ssh -Y -i ~/.ssh/id_ed25519_csf3 z29707aj@csf3...` |

`-Y` is X11 only; `-i` is the identity file.

## Hugging Face Hub

- **Do not** use `curl hf.co/cli/install.sh` before `module load miniforge` (needs Python 3.10+).
- **Pin** `huggingface_hub` **&lt; 1.0**. Version **2.x** breaks downloads (`TypeError: process() takes no keyword arguments` with `httpx2`).

```bash
module load miniforge
python -m pip install --user "huggingface_hub>=0.26,<1.0"
export PATH="$HOME/.local/bin:$PATH"
hf auth whoami    # expect: Absatron (token stored under ~/.cache/huggingface/ on CSF home)
```

Smoke test:

```bash
hf download reesekneeland/MIRAGE .gitattributes \
  --repo-type dataset --local-dir /tmp/hf-smoke
```

**Weights destination (project):**

```bash
SCRATCH=~/scratch/comp30030-mirage-ablation
mkdir -p "$SCRATCH/data/frozen_weights/mirage_hf"
# Use snapshot_download / hf download with allow_patterns per prerequisites doc
```

HF auth lives on **CSF home**, not the laptop. Do **not** commit tokens; `.env` in the git repo is for local-only secrets if needed.

## AWS CLI (NSD S3)

No personal AWS account required for the public bucket:

```bash
# One-time install (user-local):
curl -fsSL https://awscli.amazonaws.com/v2/install.sh | bash
export PATH="$HOME/.local/bin:$PATH"

aws s3 ls s3://natural-scenes-dataset/ --no-sign-request
```

**Sync target:**

```bash
SCRATCH=~/scratch/comp30030-mirage-ablation
# Dry-run first; see docs/execution/data-and-compute-prerequisites.md
aws s3 sync --dryrun --no-sign-request \
  s3://natural-scenes-dataset/nsddata/experiments/nsdimagery/ \
  "$SCRATCH/data/raw/nsd_imagery/metadata/"
```

Run large syncs via **Slurm** when possible (login node = staging only, no heavy compute).

## Scratch storage (`~/scratch`)

| Topic | Detail |
|-------|--------|
| Path | `~/scratch/comp30030-mirage-ablation` → `/net/scratch/z29707aj/comp30030-mirage-ablation` |
| Quota | **No per-user TB quota** on scratch (fair use on shared Lustre ~1.9 PB pool) |
| Cleanup | Files **not read/written for 3 months** may be auto-deleted; **not backed up** |
| Archive | Copy important results to **home** or **RDS** per `docs/CSF/response.md` |

Check space:

```bash
df -h ~/scratch
du -sh ~/scratch/comp30030-mirage-ablation
```

## Agent command template (from Mac)

Prerequisite: `ssh -O check csf3` → `Master running`.

```bash
ssh csf3 'module load miniforge; export PATH=$HOME/.local/bin:$PATH; cd ~/comp30030-mirage-ablation && git pull && aws s3 ls s3://natural-scenes-dataset/ --no-sign-request | head -3'
```

## Slurm

Smoke-tested 2026-10-21: `scripts/csf/slurm_smoke.sbatch` job `23495544` (serial, exit `0:0`). `csf.slurm_tutorial_complete: true` in `runs/registry.yaml`.

### M1 perception beta sync (`sync_m1_perception_subj.sbatch`)

| Topic | Detail |
|-------|--------|
| **Workload** | `aws s3 sync` of one subject’s NSD `betas_fithrf` (~45–65 GB) — **I/O-bound**, not multi-core compute |
| **Partition** | **`serial`** (`#SBATCH -p serial`, 1 CPU). Do **not** use `multicore` for this script |
| **Why not multicore** | On CSF3 (2026-10-26), `multicore` jobs with 2 CPUs sat **PENDING (Priority)** for hours with Slurm **estimated start ~4 days** ahead; identical work on **`serial` started within ~1 minute** |
| **Submit** | One subject at a time: `sbatch --export=SUBJ=02 scripts/csf/sync_m1_perception_subj.sbatch` (repeat `03`…`08`) |
| **Runtime** | ~7–15 minutes active sync per subject once the job is **RUNNING** (subj01 serial-equivalent: ~7m on multicore when queue was short) |
| **Monitor** | `squeue -u $USER`; `sacct -j JOBID -X`; `tail slurm-m1-subj-JOBID.out`; `du -sh ~/scratch/.../data/raw/nsd/betas/subjNN` |
| **Transient failures** | `AWS_IO_SOCKET_TIMEOUT` near end of sync → job **FAILED** with partial scratch; **re-sbatch same SUBJ** (sync resumes). Script retries up to 3 passes with adaptive AWS retries. |
| **Queue diagnosis** | `scontrol show job JOBID` → `Reason=` and `StartTime=` (estimated). `Reason=Priority` on `multicore` ≠ script failure |

**Later stages** still use **`multicore`**, **high-memory**, or **GPU** partitions for ingest, ridge, and diffusion (see execution plan § CSF3).
