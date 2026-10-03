# Hypothesis Formulation: What Enables Perception-to-Imagery Generalization in fMRI Vision Decoders?

**Date:** 2026-09-06  
**Status:** Investigator-approved — primary H₀ (Option A), secondary H₀ (Option D), exploratory (Option C); automated latent metrics confirmed. Pending `experimental-design` only.  
**Source proposal:** `docs/proposal/new_proposal.md`  
**Next step:** `experimental-design`

---

## Research proposal summary

This project investigates **which latent representations best support perception-trained fMRI vision decoders when tested on mental imagery**. The experimental platform is fixed: the **NSD-Imagery** benchmark (7T fMRI; perception and imagery tasks) and the open-source **MIRAGE** pipeline (ridge-regression backbone, frozen Stable Cascade diffusion). The **only deliberate variation** is the neural-to-latent mapping target:

1. CLIP **image** embeddings only  
2. CLIP **text** embeddings only  
3. **Combined** image and text embeddings  

Evaluation is **two-stage**:

- **Decoder-quality (pre-generation):** three **automated** latent metrics on predicted embeddings *before* diffusion — **top-k retrieval accuracy**, **cosine similarity** to ground-truth embedding, and **automated embedding 2AFC** (rule-based argmax of cosine similarity between ground-truth vs distractor candidate in latent space; not human raters, not an AI agent) — reported per subject and stimulus type (simple, complex, conceptual).  
- **Reconstruction-quality (post-generation):** CLIP 2WC, SSIM, PixCorr on images produced by the same frozen diffusion model.

The cross-task protocol trains exclusively on NSD **perception** trials and tests on NSD-Imagery **imagery** trials, with preprocessing and hyperparameter selection confined to training data. A stricter stimulus-level holdout (excluding imagery targets from perception training) is planned where feasible.

**Success criteria (from proposal):** identify which latent targets most reduce the perception-to-imagery gap, and determine whether apparent generalisation gains reflect genuine neural decoding or compensation by a frozen generative prior.

**Deliverables:** reproducible ablation codebase (MIRAGE fork), quantitative comparison of decoder vs reconstruction metrics, written report.

---

## Research question

**Primary:** Among CLIP image-only, CLIP text-only, and combined CLIP image+text latent targets — holding backbone, diffusion model, and training protocol fixed — which representation(s) yield the best **neural-to-latent decoding** of mental imagery from perception-trained models, and do reconstruction gains track those latent-space gains or diverge (indicating generative-prior compensation)?

**Secondary (registered):** Do differences among latent-target conditions in reconstruction metrics persist after accounting for decoder-quality differences — indicating generative-prior compensation or multimodal conditioning synergy rather than neural decoding alone?

**Exploratory (underpowered):** Do latent-target effects interact with stimulus type (simple vs complex vs conceptual)? Descriptive or exploratory analysis only; not a formally registered hypothesis.

---

## Cognitive gap

Recent work establishes that **perception-trained decoders can generalise to mental imagery**, but that **vision SOTA does not predict imagery SOTA** and that **decoder design dominates cross-task performance** (Kneeland et al., CVPR 2025; Kneeland et al., PLoS Comput Biol 2026). MIRAGE specifically shows that a linear backbone with compact, multimodal CLIP guidance achieves state-of-the-art imagery reconstruction on NSD-Imagery, and that **image-only guidance outperforms text-only, while combined guidance outperforms either alone** — especially for imagery (Kneeland et al., 2026).

However, three gaps remain that this project targets:

1. **Latent decoding vs generative compensation is not isolated.** MIRAGE evaluates guidance-modality ablations primarily through **post-diffusion reconstruction metrics** (e.g., normalised metric averages in Fig. 4B). A strong frozen diffusion prior can produce plausible images even when decoded brain representations are weak (a concern MIRAGE partially addresses via **human** 2AFC with matched priors and low-guidance controls, but not via systematic pre-diffusion latent evaluation per ablation condition). The proposal's core novelty is to **measure decoder quality on predicted CLIP latents before generation** and compare against reconstruction metrics under identical conditions.

2. **Modality-specific contributions to cross-task transfer are not quantified at the representation level.** MIRAGE motivates text guidance neuroscientifically (higher-level visual cortex overlap with imagery; language-supervised encoding models) and image guidance empirically (compact CLS-token embeddings vs high-dimensional patch tokens that fail on low-SNR imagery). Yet it does not report **retrieval, cosine similarity, or automated latent 2AFC on decoded image vs text vs combined embeddings separately** for imagery trials. Without this, it remains unclear whether combined guidance helps because the brain decodes both modalities well, or because Stable Cascade exploits multimodal conditioning even when one stream is poorly decoded.

3. **Cross-task generalisation is conflated with stimulus overlap.** Some NSD-Imagery targets also appear in NSD perception training. NSD-Imagery and supervisor feedback note that perception-to-imagery transfer and **unseen-stimulus generalisation** should be reported separately. The proposal's optional strict holdout addresses a gap neither MIRAGE nor the benchmark paper fully resolves.

**In one sentence:** We know multimodal CLIP guidance helps imagery *reconstruction* under MIRAGE, but we do not know **how much each latent target contributes to genuine cross-task neural decoding** versus **downstream generative prior effects**, nor how those contributions vary by stimulus type and training overlap.

---

## Registered hypotheses (investigator-approved)

Hypothesis framing is **human-owned**. The investigator has registered the following primary, secondary, and exploratory statements. Decoder-quality metrics are **automated only** (no human raters in this study's evaluation battery).

### Decoder-quality metrics (pre-generation, all registered H₀ tests)

| Metric | Definition |
|--------|------------|
| Top-k retrieval accuracy | Rank of ground-truth embedding within retrieved candidates |
| Cosine similarity | Cosine distance between predicted and ground-truth embedding |
| Automated embedding 2AFC | Rule-based argmax(cosine similarity) between ground-truth vs distractor candidate in latent space — **not** human raters, **not** an AI agent |

*Prior work (NSD-Imagery, MIRAGE) reports **human** 2AFC with large rater panels as a reconstruction benchmark convention; that protocol is cited for context but is **not** part of this study's evaluation battery.*

---

### Primary — Option A: No latent-target advantage

**H₀ (primary):** Under a fixed MIRAGE backbone and frozen Stable Cascade, there is **no significant difference** in imagery-trial decoder-quality metrics among CLIP image-only, text-only, and combined latent-target conditions.

**H₁ (primary):** At least one latent-target condition differs significantly from the others (**two-sided omnibus** test + **pre-registered pairwise post-hocs** for full ranking: image vs text, image vs combined, text vs combined).

*Implication if H₀ is rejected:* Latent-space decoding differences drive condition effects; if reconstruction differs without corresponding latent differences, generative compensation is implicated (see secondary H₀).

---

### Secondary — Option D: Reconstruction tracks latent decoding

**H₀ (secondary):** Differences among latent-target conditions in **reconstruction metrics** (CLIP 2WC, SSIM, PixCorr) are **fully explained by** differences in decoder-quality metrics (no significant residual condition effect after accounting for latent-space performance).

**H₁ (secondary):** Reconstruction-metric differences **persist after** controlling for latent decoding quality (evidence of generative-prior compensation or multimodal conditioning synergy).

*Rationale:* Directly operationalises the proposal's aim to separate neural decoding from generative compensation.

---

### Exploratory — Option C: Stimulus-type interactions (not formally registered)

**Exploratory question:** Does the rank ordering of latent-target conditions on decoder-quality metrics differ across simple, complex, and conceptual imagery stimulus types?

*Rationale:* NSD-Imagery varies stimulus complexity; higher-level cortex shows stronger perception–imagery alignment than early visual cortex. Text guidance might help more for conceptual stimuli; image guidance might help more for simple/complex.

*Status:* **Underpowered** (6 stimuli per type); analysis is **descriptive or exploratory only** — not a registered primary or secondary hypothesis.

---

### Demoted framing — Option B (not a registered hypothesis)

Combined vs each single-modality comparison is covered by **primary H₀ post-hocs** (image vs combined, text vs combined). Whether combined decoding outperforms the better single-modality condition (MIRAGE-aligned ordering: combined > image > text at reconstruction) may be discussed in **Results/Discussion** without separate H₀ registration.

---

## Domain and data constraints

Constraints below are **biological, data-collection, and platform limits** — not experimental protocols (splits, CV, and evaluation design belong in `experimental-design`).

### Neuroimaging and task constraints

| Constraint | Detail | Source |
|------------|--------|--------|
| Modality | 7T fMRI BOLD | NSD-Imagery extends NSD acquisition protocol |
| SNR | Mental imagery has **lower SNR** and coarser effective spatial resolution than perception, especially in early visual cortex | Kneeland et al. 2025; neuroimaging literature cited therein |
| Task design | Imagery: 4 s trials, letter cue, vividness rating; vision: viewed stimuli in frame | NSD-Imagery benchmark |
| Stimulus sets | 6 simple + 6 complex + 6 conceptual targets; **18 imagery stimuli** total per subject | NSD-Imagery |
| Conceptual stimuli | No single ground-truth image; vision trials for conceptual set are **not recommended** for benchmark evaluation | Kneeland et al. 2025 |
| Cross-decoding necessity | Imagery dataset too small for imagery-only training at scale; evaluation is **train perception → test imagery** | NSD-Imagery; MIRAGE |

### Subject and sample constraints

| Constraint | Detail |
|------------|--------|
| NSD-Imagery collection | 8 participants from original NSD |
| Decoder benchmark convention | Subjects **1, 2, 5, 7** completed full NSD and are standard for model training/evaluation |
| Trial volume | 576 trials/subject across run types; imagery runs completed twice |
| Statistical power | **Very small N** at stimulus level (6 per type) and subject level (4) limits fine-grained inference |

### Representational and platform constraints

| Constraint | Detail |
|------------|--------|
| Fixed backbone | Ridge regression (MIRAGE default) — proposal holds this fixed for core ablations |
| Fixed generator | **Stable Cascade frozen** throughout — isolates neural-to-latent mapping |
| Latent spaces | CLIP ViT-L/14 image CLS (1×768); CLIP ViT-bigG/14 text (77×1280); combined uses both |
| Auxiliary MIRAGE components | VDVAE low-level module, retrieval pool, synthetic captions (LLaVA) are part of full MIRAGE — ablations vary **guidance latents**; extensions may toggle VDVAE/ROI (proposal §5) |
| Training data overlap | Some imagery targets may appear in NSD perception training — affects interpretation of "generalisation" vs "recognition" |
| Caption dependency | Text latents derive from **synthetic captions** at train time; imagery inference uses decoded text, not ground-truth captions |

### Compute, access, and timeline

| Constraint | Detail |
|------------|--------|
| Data access | NSD-Imagery via [naturalscenesdataset.org](https://naturalscenesdataset.org) |
| Codebase | MIRAGE open source: [github.com/MedARC-AI/MIRAGE](https://github.com/MedARC-AI/MIRAGE) |
| Reproducibility | 10 reconstruction samples averaged in benchmark convention; **human** 2AFC (500 raters) used in prior NSD-Imagery/MIRAGE work only — this study uses **automated** latent metrics (retrieval, cosine, embedding 2AFC) for decoder-quality evaluation |
| Scope | Core study is ablation + evaluation; extensions (MLP backbone, VDVAE on/off, ROI masks) are **conditional on time** |

### Ethical and interpretive constraints

- Mental imagery content may **diverge from cued stimulus**; ground-truth image comparison is an imperfect proxy for subjective experience (acknowledged in NSD-Imagery discussion).  
- Decoder outputs are **research measurements**, not clinical readouts; misuse and consent concerns noted in MIRAGE discussion.

---

## Prior work summary

### NSD-Imagery benchmark (Kneeland et al., CVPR 2025)

NSD-Imagery extends NSD with 7T fMRI from the same participants during **vision, imagery, and attention** tasks across simple, complex, and conceptual stimulus sets. It enables the first large-scale test of **NSD-trained, open-source decoders** (Brain Diffuser, MindEye1, MindEye2, iCNN, Takagi et al.) on mental imagery.

**Key findings relevant to this project:**

- **Method-level decoupling:** Vision decoding performance does **not** predict imagery decoding performance across methods (e.g., MindEye2 near-chance on imagery 2AFC despite strong NSD vision results).  
- **Architecture matters:** Linear/simple backbones and multimodal features associate with better cross-task generalisation; complex architectures appear to overfit perception training.  
- **Stimulus-level correlation:** Per-stimulus reconstruction quality correlates between vision and imagery, but method rankings do not.  
- **Complexity vs distribution:** For tested methods, **training-distribution alignment** may matter more than raw stimulus complexity for imagery reconstruction ceilings.  
- **Evaluation precedent:** Low-level (PixCorr, SSIM) and high-level (AlexNet/Inception/CLIP 2WC, Eff, SwAV) metrics; brain correlation in early vs higher visual cortex; human 2AFC identification.  
- **Explicit future-work call:** Optimal decoding architectures for perception→imagery transfer remain **under-explored** — directly motivating controlled ablations.

**Gaps relative to this proposal:** No CLIP image vs text vs combined ablation under one fixed protocol; no latent-space evaluation before generation; no strict stimulus-level holdout analysis.

### MIRAGE (Kneeland et al., PLoS Comput Biol 2026)

MIRAGE is an NSD-trained decoder using **parallel ridge regressions** from fMRI to VDVAE latents, CLIP image CLS embeddings, and CLIP text embeddings, with **Stable Cascade** for final reconstruction and a retrieval module selecting among candidate generations.

**Key findings relevant to this project:**

- **SOTA imagery reconstruction** on NSD-Imagery across feature metrics and human 2AFC (significant vs distractors with matched diffusion prior).  
- **Linear backbone + compact image embeddings + multimodal guidance** identified as critical for generalisation; high-dimensional MindEye2-style image embeddings fail on imagery.  
- **Guidance modality ablation (reconstruction-level):** image-only > text-only; **combined >> either alone**, especially for imagery.  
- **Low-level VDVAE module** provides much structure even for low-resolution imagery; minimal diffusion guidance still yields identifiable reconstructions — increasing guidance mainly improves quality, not semantic identity.  
- **Neuroscientific interpretation:** Lower-dimensional image targets suit low-SNR imagery; text targets higher-level, language-aligned cortex overlap with imagery.  
- **Prior contribution controls:** 2AFC with prior-matched distractors; guidance-strength ablation — but **not** per-condition latent retrieval/cosine/2AFC before diffusion.

**Gaps relative to this proposal:** Guidance ablations reported as aggregated reconstruction metrics, not full per-metric tables per condition; **no systematic pre-diffusion evaluation** of decoded CLIP embeddings by modality; does not separate stimulus-overlap from strict OOD imagery targets.

### Broader methodological context

- **Latent-space retrieval and cosine similarity** are established fMRI decoding metrics (MindEye/MindEye1/MindEye2: contrastive CLIP mapping, top-k retrieval, 2AFC-style embedding comparisons) — but typically on **perception** data, not as cross-task ablation diagnostics.  
- **Diffusion priors** can align embeddings for reconstruction while retrieval-focused embeddings preserve fine-grained information — motivating **separate decoder vs reconstruction evaluation** (Scotti et al., NeurIPS 2023; Scotti et al., 2024).  
- **Generative compensation risk** is recognised in the field; MIRAGE mitigates at reconstruction level but the proposal pushes this further upstream.

**Synthesis:** NSD-Imagery established the benchmark and the architecture-generalisation puzzle; MIRAGE provided the best current solution and preliminary evidence that multimodal CLIP guidance helps. **This project's contribution** is not a new SOTA pipeline but a **controlled, reproducible decomposition** of *which latent target carries cross-task decoding signal* — measured where the generative prior cannot compensate.

---

## Key citations

| ID | Citation | Role |
|----|----------|------|
| [1] | Kneeland R, Scotti PS, St-Yves G, Breedlove J, Kay K, Naselaris T. **NSD-Imagery: A benchmark dataset for extending fMRI vision decoding methods to mental imagery.** CVPR 2025. [DOI: 10.1109/CVPR52734.2025.02687](https://doi.org/10.1109/cvpr52734.2025.02687) | Benchmark dataset, cross-task evaluation, architecture decoupling |
| [2] | Kneeland R, Villanueva CKT, Chen T, Ojeda J, Khanna S, Xu J, et al. **MIRAGE: Robust multi-modal architectures translate fMRI-to-image models from vision to mental imagery.** PLoS Comput Biol 22(5): e1014263, 2026. [DOI: 10.1371/journal.pcbi.1014263](https://doi.org/10.1371/journal.pcbi.1014263) | Fixed platform, guidance ablations, SOTA imagery baseline |
| [3] | Scotti PS, Banerjee A, Goode J, Shabalin S, Nguyen A, Cohen ED, et al. **Reconstructing the Mind's Eye: fMRI-to-Image with Contrastive Learning and Diffusion Priors (MindEye).** NeurIPS 2023. [arXiv:2305.18274](https://doi.org/10.48550/arXiv.2305.18274) | Latent retrieval/cosine metrics; diffusion prior vs retrieval tradeoff |
| [4] | Scotti PS, Triantafyllou C, Anderson AJ, Kneeland R, Zheng H, Deng J, et al. **MindEye2: Shared-Subject Models Enable fMRI-To-Image With 1 Hour of Data.** 2024. | High-dim embeddings; perception SOTA that fails imagery transfer |
| [5] | Allen EJ, St-Yves G, Wu Y, Breedlove J, Prince JS, Dowdle LT, et al. **A massive 7T fMRI dataset to bridge cognitive neuroscience and artificial intelligence.** Nature Neuroscience, 2022. | NSD parent dataset |
| [6] | Supervisor feedback (Jingyuan). `docs/proposal/feedback.md` | Novelty framing, OOD precision, latent-before-diffusion evaluation |

---

## Assumption ledger

| # | Assumption | Risk | Rationale / if wrong |
|---|------------|------|----------------------|
| A1 | **MIRAGE reproduction** on NSD-Imagery (perception train, imagery test) is achievable with published code and yields reconstruction performance in the same ballpark as reported | **Medium** | Environment, preprocessing, and hyperparameters may differ; failure blocks fair ablation comparison |
| A2 | **Ablating latent targets** (image / text / combined) while holding backbone and Stable Cascade frozen **isolates** neural-to-latent mapping effects | **Medium** | MIRAGE couples VDVAE, retrieval, and caption pipelines; partial ablations may leave confounding paths (e.g., retrieval uses hidden-layer image embeddings) |
| A3 | **Pre-diffusion automated latent metrics** (top-k retrieval, cosine similarity, automated embedding 2AFC) validly index neural decoding quality for each guidance stream | **Medium** | Metrics developed mainly for perception; imagery ground-truth is cued image, not subjective mental content; distractor sampling protocol TBD in experimental design |
| A4 | **Frozen Stable Cascade** limits generative compensation sufficiently to compare conditions fairly | **Medium** | Same prior for all conditions helps, but multimodal conditioning may still synergise non-linearly at generation |
| A5 | **Combined > image > text** reconstruction ordering from MIRAGE **partially transfers** to latent-space metrics on imagery | **Medium** | Core scientific question — if false, project findings are more novel |
| A6 | **Text latents from decoded captions** (not ground-truth) reflect brain-decodable semantic structure for imagery | **High** | Training uses synthetic captions; imagery inference has no stimulus — caption quality and decoding error compound |
| A7 | **Four subjects (1,2,5,7)** suffice for condition-level conclusions with proposed uncertainty quantification | **High** | Small N; stimulus-type cells have only 6 items |
| A8 | **Stimulus-type labels** (simple / complex / conceptual) map to measurably different representational demands | **Medium** | Conceptual lacks image ground truth; metrics may be semantics-only |
| A9 | **Perception-trained ridge models** generalise to imagery via shared cortical representations | **Low** | Strong neuroscientific and empirical support in cited work |
| A10 | **Strict stimulus holdout** is feasible within NSD trial structure without eliminating too much training data | **Medium** | Overlap extent needs data audit; may reduce power |
| A11 | Differences in reconstruction metrics **without** latent-metric differences indicate generative compensation | **Medium** | Retrieval module and VDVAE path also affect final images independently of CLIP guidance ablations |
| A12 | Project timeline supports core three-way ablation + dual evaluation without requiring extensions | **Low** | Scoped MVP in proposal; extensions explicitly optional |

---

## Open questions for experimental design

*These are deliberately unresolved here; `experimental-design` should address them now that H₀ framing and metrics are approved.*

1. **Stimulus overlap audit:** How many of the 18 imagery targets (and close semantic neighbours) appear in NSD perception training for subjects 1,2,5,7? How should "seen" vs "held-out" imagery targets be defined?  
2. **Latent metric specification:** Exact embedding layers for cosine/retrieval (CLS vs hidden layer; pooled vs unpooled text); retrieval pool composition (within-type, within-subject); **automated embedding 2AFC** distractor sampling protocol.  
3. **MIRAGE component handling during ablation:** When text guidance is ablated, are VDVAE, retrieval, and img2img paths unchanged? How is combined condition defined when one stream is missing — zero padding, retrained single-head, or architectural gating?  
4. **Caption pipeline:** Are synthetic captions fixed from MIRAGE training artifacts, or regenerated? Impact on text-only ablation interpretability.  
5. **Hyperparameter fairness:** Single λ (ridge) per condition vs per-condition tuning on perception validation only — how to prevent unfair advantage?  
6. **Uncertainty quantification:** Permutation baselines, bootstrap CIs, multi-seed stability — which are mandatory for the report given small N?  
7. **Conceptual stimulus evaluation:** Which metrics apply without ground-truth images (text embedding similarity to concept labels, exclusion from image-based metrics)?  
8. **Reproduction acceptance criteria:** What deviation from published MIRAGE imagery metrics still counts as successful baseline reproduction?  
9. **Secondary H₀ (Option D) linkage analysis:** Formal test for residual condition effect after controlling for latent metrics (e.g., mediation/regression of reconstruction on decoder-quality + condition) — specify model and inference given small N.  
10. **Primary H₀ statistical plan:** Omnibus test across three conditions; pre-registered pairwise post-hocs (image vs text, image vs combined, text vs combined); multiplicity correction.  
11. **Extension prioritisation:** If core ablations complete early, rank optional extensions (MLP backbone, VDVAE off, ROI masks) by informativeness vs effort.

---

## Link to paper structure (for later writing)

| Formulation section | Supports |
|---------------------|----------|
| Cognitive gap + prior work | Introduction, Related Work |
| Domain constraints | Methods (data, participants), Discussion (limitations) |
| H₀/H₁ registration | Introduction (hypotheses), Results (pre-registered contrasts) |
| Assumption ledger | Methods (design rationale), Discussion (threats to validity) |
| Open questions | Methods detail to be filled by experimental design |

---

## Approval checklist

- [x] Primary and secondary research questions confirmed  
- [x] H₀/H₁ registration approved — primary Option A, secondary Option D, exploratory Option C; Option B demoted  
- [x] Decoder-quality metrics approved — top-k retrieval, cosine similarity, automated embedding 2AFC (no human raters)  
- [x] Domain constraints accepted or amended  
- [x] Assumption ledger reviewed; high-risk items mitigated or accepted  
- [ ] Ready to invoke **`experimental-design`**
