# Model Design Comparison: Perception-to-Imagery Latent-Target Ablation

**Date:** 2026-09-09  
**Status:** **Approved — Option 3** (2026-09-10)  
**Selected:** [Option 3 — Dual-track hybrid](2026-09-06-perception-imagery-latent-ablation-option-3.md)  
**Also considered:** [Option 1](2026-09-06-perception-imagery-latent-ablation-option-1.md) · [Option 2](2026-09-06-perception-imagery-latent-ablation-option-2.md)  
**Next step:** `execution-plan`

---

## Research summary

This study holds the **ridge regression mapper** and **frozen Stable Cascade / CLIP / VDVAE** fixed (HC-01, HC-02) and varies only CLIP latent-target ablations (`image_only`, `text_only`, `combined`) under a perception-train → imagery-test protocol on NSD / NSD-Imagery [Kneeland et al., CVPR 2025; Kneeland et al., 2026]. The scientific novelty is **decoder-quality evaluation before diffusion** (S8) separated from **reconstruction evaluation after diffusion** (S10), enabling Option D linkage analysis ($R_{s,i,c} \sim D_{s,i,c} + \text{condition}$).

### Platform precedents

| Finding | Source | Implication for fork design |
| ------- | ------ | --------------------------- |
| MIRAGE uses **parallel ridge regressions** to VDVAE ($1 \times 91168$), CLIP ViT-L/14 CLS ($768$), CLIP ViT-bigG/14 text ($77 \times 1280$), and retrieval hidden ($257 \times 1024$ flattened) | Kneeland et al., PLoS Comput Biol 2026, Fig 6–7 | Head-level orchestration and inactive-head skipping are first-class design requirements |
| $\lambda = 10^5$ selected via **grid search on non-evaluation subjects** (3,4,6,8) for imagery generalisation | MIRAGE §4.2.3; experimental strategy | `lambda_tune` module must be shared across conditions with **independent $\lambda$ per active head** (HC-06) |
| **Image-only SC guidance > text-only; combined >> either** at reconstruction level | MIRAGE Fig 4B / ablation numbering | Ablation inference must apply **literal zero tensors** for ablated guidance — not architectural removal (HC-07) |
| **Linear ridge > MLP** for imagery SNR; high-dim MindEye2 embeddings fail cross-task transfer | MIRAGE 2026; NSD-Imagery 2025 | MLP backbone extension is Phase 5 only — not MVP architecture |
| Entry points: `Train.ipynb`, `recon_inference_mi.ipynb`, `final_evaluations_multi_mi.ipynb` | [MedARC-AI/MIRAGE](https://github.com/MedARC-AI/MIRAGE) | Notebook-centric Option 1 aligns with upstream; extraction target for Options 2–3 |
| MindEye separates **retrieval-optimised** CLIP embeddings from **reconstruction-optimised** diffusion-prior outputs; top-$k$ / cosine metrics index fine-grained decoding | Scotti et al., NeurIPS 2023 | Motivates **separate evaluation subpackages** for S8 vs S10 even with shared S7 latents |
| Retrieval distractor protocol: shared1000 pool, $N=50$, resampled draws | MIRAGE Fig Q; experimental strategy A2 | Decoder eval module must consume **frozen catalogues** — no test-informed pools (HC-11) |

### Failure modes relevant to architecture

| Failure mode | Architectural response |
| ------------ | ---------------------- |
| Generative prior masks weak latents | Hard S8/S10 boundary; Option D regression |
| Retrieval + VDVAE confounds ablation | Fixed across conditions; diagnostic retrieval-head metrics reported separately |
| Imagery leakage into train/$\lambda$ | Manifest-validated split builder; pre-flight asserts |
| S12 reproduction failure | Gate before ablation stats (HC-12); Option 3 maximises notebook fidelity |
| Metric/composite implementation bugs | Centralised `composite_d.py`; unit tests (Options 2–3) |

---

## Fixed constraints (not design choices)

All options must implement identically:

- Ridge mapper; three ablation conditions; zero-vector SC protocol (HC-07)
- VDVAE + retrieval heads always on across conditions
- Train perception ($s \in \{1,2,5,7\}$) → test imagery; tune $\lambda$ on $\{3,4,6,8\}$
- S8 decoder metrics before diffusion; S10 reconstruction after
- Setting A primary; Setting B secondary; S12 gate on combined Setting A
- Primary endpoint: $D_{s,i,c}$ (216 cells); z-reference pools 144 image / 144 text

---

## Option summaries

| | Option 1: Monolithic fork | Option 2: Modular package | Option 3: Dual-track hybrid |
| --- | --- | --- | --- |
| **Core idea** | Extend MIRAGE notebooks + YAML | Python packages + declarative config | Notebooks for S12 gate + Option 2 for ablation |
| **Condition switch** | Inline notebook branches | `conditions.py` + YAML | Track B: config-driven |
| **S7 latent cache** | Optional sidecars | **Mandatory** versioned cache | Mandatory on Track B |
| **S8 vs S10** | Sequential notebook sections | Separate `evaluation/` subpackages | Track B only |
| **S12 gate** | First cells in eval notebook | `reproduction_gate.py` | **Track A notebooks authoritative** |
| **MVP effort** | Lowest | Medium | Highest |
| **Ablation maintainability** | Lowest | **Highest** | Medium–high |

---

## Comparison matrix

Criteria derived from experimental strategy primary/secondary metrics, leakage controls, and pipeline non-functional requirements.

| Criterion | Option 1 | Option 2 | Option 3 | Weight |
| --------- | :------: | :------: | :------: | ------ |
| **S12 reproduction fidelity** | ●●● | ●● | ●●●● | High |
| **S8/S10 separation (HC-10)** | ●● | ●●●● | ●●●● | **Critical** |
| **Leakage-safe split enforcement** | ●● | ●●●● | ●●●● | **Critical** |
| **Fair $\lambda$ orchestration (HC-06)** | ●●● | ●●●● | ●●●● | High |
| **S7 cache → cheap S8 rerun** | ● | ●●●● | ●●●● | High |
| **Three-condition maintainability** | ●● | ●●●● | ●●● | Medium |
| **Downstream flush discipline** | ●● | ●●●● | ●●● | Medium |
| **Time to first runnable MVP** | ●●●● | ●●● | ●● | Medium |
| **Composite $D$ testability** | ●● | ●●●● | ●●●● | High |
| **Parallelisation (PF-04)** | ●●● | ●●●● | ●●● | Medium |
| **Statistical module clarity (S11)** | ●● | ●●●● | ●●●● | Medium |
| **Long-term extension hooks (Phase 5)** | ●● | ●●●● | ●●● | Low |
| **Operational complexity** | ●●●● | ●●● | ●● | — |

Legend: ● = weak · ●● = adequate · ●●● = good · ●●●● = excellent

---

## Compute / memory summary

| Stage | Dominant resource | Notes across options |
| ----- | ----------------- | -------------------- |
| S5 ridge | CPU | Identical math; Option 2 adds negligible overhead |
| S6 $\lambda$ tune | CPU + tuning imagery decode | Central module in Options 2–3 prevents unfair grids |
| S7 latent inference | GPU (CLIP) | Options 2–3: persist to `artifacts/latents/` |
| **S9 diffusion** | **GPU — dominant** | 6480 runs; all options equal |
| S8 metrics | GPU/CPU | Options 2–3 avoid S9 rerun |
| S10 metrics | GPU/CPU | MIRAGE-compatible eval |
| Option 3 overhead | +1 combined notebook run | Gate track before ablation |

---

## Risk comparison

| Risk | Opt 1 | Opt 2 | Opt 3 |
| ---- | ----- | ----- | ----- |
| Notebook/config drift across conditions | High | Low | Medium |
| S12 fail → blocked ablation | Medium handling | Medium | **Best** gate credibility |
| Package vs MIRAGE numeric drift | N/A | Medium | Medium (parity module) |
| S8 implementation error | Medium | Low | Low |
| Timeline overrun | Low | Medium | High |
| Dual-pipeline confusion | — | — | Medium |

---

## Out-of-scope extensions (all options)

Phase 5 branches use the **same frozen manifest** but are **not MVP**:

| Priority | Extension | Architecture note |
| -------- | --------- | ----------------- |
| 1 | VDVAE on/off | Config profile toggling VDVAE head + img2img path |
| 2 | ROI masks | Alternate voxel mask in ingest module |
| 3 | MLP backbone | **Excluded from core study** (HC-01) |

---

## Recommendation

**Recommended: Option 2 — Modular Config-Driven Pipeline Package**

### Evidence

1. **Primary scientific requirement:** The registered hypotheses depend on **reliable pre-diffusion decoder metrics** ($D_{s,i,c}$, 216-cell omnibus) distinct from post-diffusion $R_{s,i,c}$. Option 2 enforces this at the **import boundary** between `evaluation.decoder` and `evaluation.reconstruction`, matching the proposal's core novelty and MindEye's precedent for separating retrieval diagnostics from generative outputs [Scotti et al., 2023].

2. **Operational efficiency:** S9 diffusion dominates runtime ($6480$ samples). Mandatory S7 latent caching (Option 2) allows S8 metric iteration — composite z-scoring, distractor resampling, embedding 2AFC — **without repeating diffusion**, which Options 1 only supports optionally.

3. **Leakage and fairness:** Independent $\lambda$ per active head per condition (HC-06), manifest-hashed artifacts, and automated split validation address the highest-severity pipeline risks identified in the experimental strategy leakage checklist. Option 1 relies on notebook discipline alone.

4. **S12 gate:** Option 2's `reproduction_gate.py` should be validated against MIRAGE notebook output on combined Setting A before ablation reporting. If early replication attempts show $> \pm 0.05$ drift, **upgrade to Option 3** (dual-track) rather than Option 1 — preserving modular ablation while restoring notebook-authoritative gate metrics.

5. **Deliverable alignment:** Proposal deliverable #1 asks for a "reproducible ablation codebase with **modular latent-target and evaluation configuration**" — Option 2 maps directly; Option 1 does not.

### Not recommended as primary

- **Option 1** if the project prioritises decoder-before-diffusion rigour and Setting B parallel runs — acceptable only under severe time constraint with explicit acceptance of S8/S9 coupling and higher drift risk.
- **Option 3** unless S12 parity proves difficult after Option 2 gate implementation — adds duplication cost without hypothesis-testing benefit once parity is demonstrated.

---

## User decision

**Approved 2026-09-10:** **Option 3 — Dual-track hybrid**

Rationale: maximum S12 reproduction credibility; Track A / Track B isolation for clearer debugging if gate or ablation metrics diverge.

| Choice | Status |
| ------ | ------ |
| **Option 3** | **Selected** — dual-track; execution-plan includes parity module |
| Option 2 | Not selected (modular package retained as Track B substrate) |
| Option 1 | Not selected |

---

## Key references

| ID | Citation | Role |
| -- | -------- | ---- |
| [1] | Kneeland R, et al. NSD-Imagery. CVPR 2025. [DOI: 10.1109/CVPR52734.2025.02687](https://doi.org/10.1109/cvpr52734.2025.02687) | Benchmark splits, 2AFC distractor logic |
| [2] | Kneeland R, et al. MIRAGE. PLoS Comput Biol 22(5): e1014263, 2026. [DOI: 10.1371/journal.pcbi.1014263](https://doi.org/10.1371/journal.pcbi.1014263) | Ridge heads, $\lambda$ tuning, ablation table, Table 1 gate |
| [3] | Scotti PS, et al. MindEye. NeurIPS 2023. [arXiv:2305.18274](https://doi.org/10.48550/arXiv.2305.18274) | Latent retrieval/cosine metrics; retrieval vs reconstruction separation |
| [4] | MedARC-AI/MIRAGE. [github.com/MedARC-AI/MIRAGE](https://github.com/MedARC-AI/MIRAGE) | Upstream notebook entry points |
| [5] | `experimental_strategies/2026-09-06-perception-imagery-latent-ablation-experimental-strategy.md` | Metrics, splits, statistical plan |
| [6] | `pipeline_definitions/2026-09-06-perception-imagery-latent-ablation-pipeline-definition.md` | Stage contracts, open decisions |
| [7] | `docs/references/statistical-methods-reference.md` | $D$, $R$, permutation procedures |
