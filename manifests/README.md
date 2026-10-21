# Manifests — S0 Freeze Instructions

**Study:** perception-imagery-latent-ablation  
**Stage:** S0 (shared across Track A and Track B)  
**Authority:** `docs/workflow_stages/execution_plans/2026-09-10-perception-imagery-latent-ablation-execution-plan.md`

Manifests in this directory define the **frozen OOD test catalogue**, training exclusions, and audit artefacts. They must be populated, hashed, and investigator-signed **before any model fitting** (S5, Track A ridge training).

---

## Required files (post-S0)

| File | Purpose |
| ---- | ------- |
| `nsd_imagery_test_manifest_v1.json` | 18 imagery stimuli; subject roles; condition list; seeds |
| `stimulus_overlap_audit.json` | Per-subject exact matches, semantic neighbours ($\geq 0.85$), Setting B exclusions |
| `model_weights_manifest.json` | SHA-256 per frozen encoder checkpoint (HC-02) |
| `nsd_imagery_test_manifest_v1.sha256` | Hash sidecar |
| `stimulus_overlap_audit.sha256` | Hash sidecar |

Supporting frozen catalogues (S0.3) live under `data/frozen_catalogues/`:

- `shared1000_embeddings.npz`
- `within_type_imagery_list.json`

---

## Population workflow

Execute **once** via Track B tooling (when `mirage_ablation/` package is implemented):

```bash
# S0.1 — test manifest
python scripts/s0_populate_manifests.py \
  --output manifests/nsd_imagery_test_manifest_v1.json

# S0.2 — overlap audit
python scripts/s0_populate_manifests.py \
  --audit --threshold 0.85 \
  --output manifests/stimulus_overlap_audit.json

# S0.3 — distractor catalogues
python scripts/s0_populate_manifests.py --freeze-catalogues

# S0.4 — model weights manifest
python scripts/s0_populate_manifests.py --weights-manifest

# S0.5 — hash and verify
python scripts/s0_verify_manifests.py --write-hashes
python scripts/preflight.py
```

**Prerequisites:** NSD session manifests and NSD-Imagery stimulus documentation on disk; CLIP ViT-L/14 weights for semantic-neighbour audit; LLaVA caption files for conceptual lemma holdout.

---

## Freeze protocol (HG-0)

1. Review manifest JSON contents for correctness (18 stimuli; 6 per type; subject lists).
2. Review overlap audit: expect `exact_seen` count $= 0$ for complex stimuli under Setting A.
3. Run `python scripts/preflight.py --leakage-checklist` (target: 12/12 pass after S4).
4. Record `manifest_sha256` and `audit_sha256` in `runs/registry.yaml`.
5. **Investigator sign-off** in `runs/execution_log.md` with date and statement: *"HG-0: manifests reviewed and frozen."*
6. Git commit frozen manifests and `.sha256` sidecars.

---

## Change control

Any change to manifest version or hash **invalidates S5–S11** (both tracks) and parity reports. Run:

```bash
python scripts/stage_runner.py --flush --reason manifest_change --confirm
```

Increment `version` in `nsd_imagery_test_manifest_v1.json` and re-hash all downstream artifacts.

---

## Current status (2026-10-21)

**Populated (HG-0 not signed).** JSON + `.sha256` sidecars are in this directory from official `cue_pair_list.xlsx` + `nsd_stim_info_merged.csv`.

| Prerequisite | Status |
| ------------ | ------ |
| NSD DUA / imagery access | **Done** (investigator) |
| CSF + S3/HF access | **Done** |
| Metadata on scratch | **In progress** — M0 `sync_m0_metadata.sh` on CSF |
| S0 scripts / `mirage_ablation` | **Done** — commit `d9e745d` |
| HG-0 investigator sign-off | **Pending** — see `runs/execution_log.md` |

Re-run population after metadata path changes: `MIRAGE_ABLATION_DATA_ROOT=~/scratch/comp30030-mirage-ablation/data python scripts/s0_populate_manifests.py`
