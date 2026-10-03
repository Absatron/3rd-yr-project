# Experimental Strategy: Perception-to-Imagery Latent-Target Ablation

**Date:** 2026-09-06  
**Status:** Investigator-approved (2026-09-07) — semantic-neighbour threshold 0.85, Setting B conceptual holdout, composite endpoint confirmed. Revisit with supervisor feedback if needed.  
**Source hypothesis formulation:** `hypothesis_formulation/2026-09-06-perception-imagery-latent-ablation-hypothesis-formulation.md`  
**Source proposal:** `docs/proposal/new_proposal.md`  
**Next step:** `pipeline-definition`

---

> **Downstream flush rule:** Any change to split boundaries, metric definitions, distractor protocols, statistical decision rules, or frozen test manifest specification in this document requires a **full downstream computational flush** — all pipeline definitions, model training, and evaluation must be re-run from scratch. No post-hoc relabelling of test stimuli or conditions.

---

## Objective

Define a leakage-safe, statistically pre-registered protocol to test whether CLIP **image-only**, **text-only**, or **combined** latent targets differ in (1) automated decoder-quality on imagery trials and (2) reconstruction quality after a frozen Stable Cascade generator, using MIRAGE as the fixed platform and NSD-Imagery as the evaluation benchmark.

**Primary scientific output:** Rank latent-target conditions on pre-generation decoder metrics and determine whether reconstruction gains track latent gains (genuine decoding) or diverge (generative-prior compensation).

---

## H₀ link

| Registered hypothesis      | H₀ statement                                                                                                                  | Primary endpoint(s)                                                              | Decision rule (summary)                                                                                                                   |
| -------------------------- | ----------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| **Primary — Option A**     | No significant difference in imagery-trial decoder-quality among image-only, text-only, and combined latent-target conditions | Decoder-quality composite (top-1 retrieval + cosine similarity + embedding 2AFC) | Reject H₀ if omnibus permutation test _p_ < 0.05 **and** ≥1 Holm-adjusted pairwise post-hoc _p_ < 0.05                                    |
| **Secondary — Option D**   | Reconstruction-metric differences among conditions are fully explained by decoder-quality differences                         | Reconstruction composite (CLIP 2WC + SSIM + PixCorr) residual condition effect   | Reject H₀ if cluster-robust regression shows joint significance of condition dummies (_p_ < 0.05) after controlling for decoder composite |
| **Exploratory — Option C** | _(not registered)_                                                                                                            | Per-stimulus-type rank ordering                                                  | Descriptive only — no confirmatory threshold                                                                                              |

Individual metrics are reported as **secondary confirmatory** endpoints for Option A (each tested with the same omnibus + pairwise structure) and as **components** of the Option D linkage model.

---

## Data domains

| Domain                            | Role                                                   | Source (this study)                                                                  | Allowed in training?                                          |
| --------------------------------- | ------------------------------------------------------ | ------------------------------------------------------------------------------------ | ------------------------------------------------------------- |
| **NSD perception (train)**        | Ridge-regression fitting; VDVAE/retrieval head fitting | NSD core sessions 1–40 for subjects **1, 2, 5, 7**; **exclude shared1000** image IDs | **Yes**                                                       |
| **NSD perception (tuning)**       | Hyperparameter (λ) selection only                      | NSD core sessions for subjects **3, 4, 6, 8**; exclude shared1000                    | **Tuning only** — never final evaluation                      |
| **NSD-Imagery imagery (test)**    | Primary evaluation — decoder + reconstruction          | 18 imagery stimuli × 4 subjects; 16 trial repetitions averaged per stimulus          | **Evaluation only**                                           |
| **NSD-Imagery vision**            | Supplementary sanity check (not hypothesis-testing)    | 12 vision stimuli (simple + complex)                                                 | **Evaluation only**                                           |
| **NSD shared1000**                | Retrieval distractor pool; overlap audit reference     | 1000 held-out NSD images                                                             | **Never training**; allowed as **fixed distractor catalogue** |
| **MIRAGE caption artifacts**      | Fixed training-time text targets                       | Precomputed LLaVA v1.5-13B synthetic captions bundled with MIRAGE release            | **Training targets only**                                     |
| **Stable Cascade / CLIP / VDVAE** | Frozen generative and encoding priors                  | MIRAGE default checkpoints                                                           | **Frozen** — no fine-tuning                                   |

**Subjects in scope:** 1, 2, 5, 7 (decoder train + test). Subjects 3, 4, 6, 8 (λ tuning only).

**Preprocessing:** GLMsingle v3 betas, 1.8-mm resolution, `nsdgeneral` voxel mask; per-run z-scoring within NSD-Imagery runs (vision vs imagery runs scored separately), matching NSD-Imagery benchmark convention [Kneeland et al., CVPR 2025; Kneeland et al., PLoS Comput Biol 2026].

---

## Split protocol

### Core cross-task split (primary)

| Stage | Data                       | Rule                                                                                       |
| ----- | -------------------------- | ------------------------------------------------------------------------------------------ |
| Train | NSD perception trials      | All perception trials for subject _s_ ∈ {1,2,5,7}, **excluding shared1000 COCO image IDs** |
| Test  | NSD-Imagery imagery trials | All 18 imagery stimuli for the same subject _s_                                            |
| Tune  | NSD perception trials      | Subjects 3,4,6,8, same exclusion rule                                                      |

**No imagery trial** enters training, λ tuning, PCA, or normalisation fitting.

### Stimulus overlap audit and seen vs held-out labels

**Audit procedure (mandatory before first model fit):**

1. Map each of the 18 NSD-Imagery imagery targets to a canonical identifier:
   - **Simple (6):** synthetic shape ID (not in COCO).
   - **Complex (6):** COCO/`shared1000` image ID for the 5 natural scenes + artwork ID for Kehinde Wiley _The Two Sisters_.
   - **Conceptual (6):** concept label string (no image ID).
2. For each subject _s_ ∈ {1,2,5,7}, query NSD training manifests (sessions 1–40, excluding shared1000) for **exact image ID matches**.
3. Compute **semantic-neighbour overlap:** for each complex imagery target embedding (CLIP ViT-L/14 CLS), flag training images with cosine similarity ≥ **0.85** [unverified threshold — standard CLIP neighbourhood criterion; sensitivity analysis at 0.80 and 0.90 required in report].
4. Write results to frozen manifest `manifests/stimulus_overlap_audit.json` (see Frozen test manifest spec).

**Seen vs held-out definitions:**

| Label                  | Rule                                                             | Expected count (approx.)                                                                                              |
| ---------------------- | ---------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| **Exact-seen**         | Exact COCO image ID present in subject's NSD perception training | **0** for standard split (complex scenes drawn from shared1000, which is excluded from training) — verify empirically |
| **Semantic-neighbour** | No exact match but ≥1 training image with CLIP CLS cosine ≥ 0.85 | Audit-dependent                                                                                                       |
| **Strict-held-out**    | Neither exact nor semantic-neighbour                             | Remaining stimuli                                                                                                     |
| **Non-image**          | Simple + conceptual (no single GT image)                         | 12 stimuli                                                                                                            |

**Dual reporting (supervisor requirement):**

- **Setting A (benchmark-aligned):** Train excluding shared1000 only — primary pre-registered analysis.
- **Setting B (strict stimulus holdout):** Additionally remove from training (a) exact imagery target IDs, (b) all semantic-neighbour images (cosine ≥ 0.85), and (c) for **conceptual** imagery targets only — see **Conceptual holdout (Setting B)** below. Secondary analysis — same metrics and tests, separately reported.

**Conceptual holdout (Setting B) — what “concept lemma” means:**

NSD-Imagery **conceptual** stimuli are **six single-word concept labels** (not fixed images), e.g. *stripes*, *banana*, *mammal* (full list frozen in `manifests/nsd_imagery_test_manifest_v1.json`). The subject imagines that concept from a letter cue.

A **lemma** here means the **canonical concept word** for that imagery target — the label string itself (case-insensitive), not a linguistic parse.

For each conceptual target with lemma `w` (e.g. `banana`):

1. Take every NSD **perception-training** image (for that subject, Setting B exclusions already applied).
2. Look up its **LLaVA synthetic caption** (same caption artifacts MIRAGE uses for text-ridge training).
3. **Remove** that training image if the caption **contains** `w` as a substring (case-insensitive).

**Example:** If the imagery concept is `banana`, remove any training image whose LLaVA caption includes “banana” (e.g. “a bowl of fruit with bananas on the table”).

**Intent:** Approximate “no training exposure to this concept” when there is no single COCO image ID to hold out (conceptual stimuli have no ground-truth image).

**Caveats (report in Methods/Discussion):** substring matching can **over-remove** (e.g. `mammal` matching “mammalian”) or **under-remove** (synonyms not containing the lemma). This is a pragmatic strict-holdout proxy, not a MIRAGE-published rule — sensitivity analysis optional.

### Train/validation inside training subjects

No random trial split within subjects for final evaluation. λ selection uses **held-out subjects 3,4,6,8** only (MIRAGE convention), not a within-subject validation fold.

---

## CV design

| Parameter                    | Value                                                                                                                          | Rationale                                                                         |
| ---------------------------- | ------------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------- |
| Cross-validation type        | **None for final test** — single frozen imagery test set                                                                       | Benchmark convention; N too small for nested CV on imagery                        |
| Hyperparameter CV            | **Between-subject** — fit on subjects 3,4,6,8, evaluate imagery-trial proxy metric on those subjects' NSD-Imagery imagery runs | Matches MIRAGE §4.2.3                                                             |
| λ search grid                | Log-spaced: **{10³, 10⁴, 10⁵, 10⁶, 10⁷}**                                                                                      | MIRAGE Appendix Fig A uses logarithmic grid; selected λ = 10⁵ in original work    |
| λ selection criterion        | Maximize **decoder-quality composite** (defined below) on tuning subjects' imagery trials, averaged across all 18 stimuli      | Aligns tuning objective with primary endpoint                                     |
| λ fairness across conditions | **Independent λ per condition per ridge head** (image CLS, text, VDVAE, retrieval hidden-layer), same grid and tuning subjects | Prevents one condition gaining advantage from a λ better suited to another stream |
| Multi-seed stability         | **3 diffusion seeds:** `{42, 123, 456}`                                                                                        | Supervisor-requested repeated seeds                                               |
| Reconstructions per seed     | **10** per stimulus (MIRAGE/NSD-Imagery convention)                                                                            | Report mean over 10 × 3 seeds = 30 samples for reconstruction metrics             |
| Trial averaging              | Mean beta across **16 imagery repetitions** per stimulus before decoding                                                       | NSD-Imagery imagery protocol                                                      |

---

## Metric definitions

### A. Decoder-quality metrics (pre-generation, automated only)

Computed on **ridge-predicted embeddings before Stable Cascade**, per subject × stimulus × condition.

#### A1. Embedding spaces (resolves open question #2)

| Stream                                                               | Layer / pooling                                             | Dimension                | Used for                                                     |
| -------------------------------------------------------------------- | ----------------------------------------------------------- | ------------------------ | ------------------------------------------------------------ |
| **Image guidance**                                                   | CLIP ViT-L/14 **CLS token**                                 | 1 × 768                  | Image-only and combined conditions — cosine, retrieval, 2AFC |
| **Text guidance**                                                    | CLIP ViT-bigG/14: **77 × 1280** at inference (Stable Cascade); **mean-pooled → 1 × 1280** for metrics only | 77×1280 (pipeline) / 1280 (metrics) | Text-only and combined — cosine, retrieval, 2AFC |
| **Retrieval head** _(reported separately, not in primary composite)_ | CLIP ViT-L/14 **hidden layer** (257 tokens = 1 CLS + 256 patches) flattened + L2-normalised | 257 × 1024 → unit vector | Diagnostic only — confound check |

**Mean-pooling (text metrics):** average the 77 token vectors element-wise → one 1280-d vector:

$$
\bar{\mathbf{t}} = \frac{1}{77}\sum_{k=1}^{77} \mathbf{t}_k
$$

Stable Cascade still receives the full **77 × 1280** decoded text tensor. Mean-pooling is used **only** so cosine / retrieval / 2AFC can compare single vectors; it discards token-level structure (acceptable for metrics; generation is unaffected).

All vectors **L2-normalised** before cosine computations. See `docs/references/statistical-methods-reference.md` (L2 normalisation).

#### A2. Top-k retrieval accuracy

**Protocol** (adapted from MIRAGE Fig Q [Kneeland et al., 2026]):

- **Query:** subject's predicted embedding for target stimulus _i_.
- **Candidate pool:** ground-truth embedding of _i_ plus **N = 50** distractor embeddings sampled uniformly **without replacement** from the **NSD shared1000** pool, encoded in the **same layer** as the query.
- **Distance:** cosine similarity (higher = closer).
- **Success:** ground truth ranks in top **k**.
- **k values reported:** **k = 1** (primary), k = 5, k = 10 (secondary).
- **Chance (k=1):** 1/(N+1) = **1/51 ≈ 0.0196** — this is **expected accuracy under random guessing**, not a statistical significance threshold (see §Decision thresholds; significance uses permutation _p_-values at α = 0.05).
- **Distractor resampling:** **100** independent random draws of the N = 50 distractor set per stimulus (MIRAGE Fig Q convention); report **mean** top-1 accuracy across draws and 95% CI across draws. This is Monte Carlo averaging over distractor noise — **not** subject-level bootstrap.

**Stimulus-type constraint:** Distractors are **not** restricted to stimulus type (shared1000 pool is all natural scenes) for primary analysis. **Sensitivity analysis:** within-type distractors only (other complex scenes) reported in appendix.

#### A3. Cosine similarity

- **Value:** cos(predicted, ground_truth) after L2 normalisation.
- **Range:** [−1, 1]; report per subject × stimulus × condition.
- **Ground truth for conceptual stimuli:** CLIP text embedding of prompt **"a photo of {concept_label}"** (ViT-bigG/14), mean-pooled — **not** an image embedding.

#### A4. Automated embedding 2AFC

**Protocol** (latent-space analogue of NSD-Imagery 2AFC distractor logic [CVPR 2025 supplement §A.5.2]):

- **Trial:** compare cos(pred, **GT embedding**) vs cos(pred, **distractor embedding**).
- **Decision:** success if cos(pred, GT) > cos(pred, distractor).
- **Distractor:** ground-truth embedding of a **different imagery stimulus of the same stimulus type** (5 choices per target).
- **Sampling:** all **5** within-type distractors evaluated per target; accuracy = fraction correct.
- **Chance:** **0.5**.
- **Condition-specific embedding space:** image metrics use image CLS; text metrics use mean-pooled text; combined condition evaluates **both streams separately** (two 2AFC scores), then averages for combined composite.

**Not human raters. Not an LLM judge.**

#### A5. Decoder-quality composite (primary endpoint for Option A)

**What “composite” means:** one **unitless summary score** per subject × stimulus × condition, combining the three decoder metrics (top-1 retrieval, cosine similarity, embedding 2AFC) after standardising each metric to comparable scale. This is the **primary value** fed into the omnibus permutation test — not the raw metrics individually (those are reported as secondary confirmatory endpoints).

**What a z-score is:** for each raw metric, transform every applicable cell to $z = (x - \mu) / \sigma$, where $\mu$ and $\sigma$ are the mean and SD across all cells **where that metric is defined for that modality**:

| Modality | Cells included in $\mu$, $\sigma$ | Count |
|----------|-------------------------------------|-------|
| Image-stream metrics | image-only + combined (all subjects, all 18 stimuli) | **144** |
| Text-stream metrics | text-only + combined (all subjects, all 18 stimuli) | **144** |

A z-score is **not** a percentage and **not** bounded to [0, 1]. Mean z ≈ 0, SD ≈ 1 across the reference set. Negative z = below-average decoding; positive z = above-average.

**Per-stream composite** (image stream or text stream):

$$
D^{\text{stream}}_{s,i,c} = \frac{1}{3}\left(z(\text{top-1}) + z(\cos) + z(\text{2AFC})\right)
$$

**Per-condition final composite** $D_{s,i,c}$ (one value per cell — **216 cells** total for the omnibus test: 4 subjects × 18 stimuli × 3 conditions):

| Condition | Definition |
|-----------|------------|
| **image-only** | $D_{s,i,c} = D^{\text{image}}_{s,i,c}$ — decoded **image CLS** only (72 cells) |
| **text-only** | $D_{s,i,c} = D^{\text{text}}_{s,i,c}$ — decoded **text** only (72 cells) |
| **combined** | $D_{s,i,c} = \frac{1}{2}\left(D^{\text{image}}_{s,i,c} + D^{\text{text}}_{s,i,c}\right)$ — both streams on the **same 72 combined-condition trials**, then averaged |

**Important:** combined does **not** average the image-only condition with the text-only condition. It scores both modalities **within** the combined run on the same trials.

**Equal weighting note:** the composite uses equal weight (⅓ per metric; 50/50 image vs text streams in combined). This is an **evaluation convention** for fair comparison across ablation conditions — it does **not** assert that Stable Cascade internally weights image and text guidance equally during diffusion.

**Permutation test:** operates on the final $D_{s,i,c}$ values (216 cells), not on raw metrics. See `docs/references/statistical-methods-reference.md`.

**Metric aggregation rationale (investigator-approved 2026-09-09):**

- **Z-reference vs z-score:** For each raw metric (e.g. image-stream cosine), compute $\mu$ and $\sigma$ over the **z-reference pool** (144 cells where that stream is measured). Each subject × stimulus × condition cell then gets an individual z-score relative to that reference. This puts image-only and combined image-branch scores on a common scale; text-only and combined text-branch scores on a separate common scale.
- **Combined is a summary, not a third latent:** $D_{\text{combined}}$ averages the image-stream and text-stream composites on the same 72 trials. Combined contributes raw image metrics to the image z-reference and raw text metrics to the text z-reference — final $D$ values do not feed back into those pools.
- **Reporting plan:** **Primary** inference uses the composite $D_{s,i,c}$ (216 cells) for the pre-registered omnibus test. **Secondary confirmatory** inference repeats omnibus + Holm post-hocs on top-1 retrieval, cosine, and embedding 2AFC **individually** (MIRAGE/MindEye convention). Results narrative should lead with per-metric tables where helpful.
- **Supervisor feedback escape hatch:** If advised to drop the composite endpoint, promote individual-metric tests to primary and retain composite as supplementary — no change to raw metric computation required.
- **Optional sensitivity (appendix):** Z-score image metrics using image-only (72) as reference only, then apply to combined; same for text-only (72) → combined.

---

### B. Reconstruction-quality metrics (post-generation)

Applied to final retrieved reconstruction after frozen Stable Cascade + retrieval module.

| Metric       | Definition                                                                                                                                                                                                                                              | Stimuli               | Primary?  |
| ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------- | --------- |
| **CLIP 2WC** | See **B1** below | Simple + complex only | **Yes**   |
| **SSIM**     | Structural similarity vs GT image; mean over 10 × 3                                                                                                                                                                                                     | Simple + complex only | Secondary |
| **PixCorr**  | Pearson correlation of flattened pixels vs GT; mean over 10 × 3                                                                                                                                                                                         | Simple + complex only | Secondary |

#### B1. CLIP 2WC (two-way comparison) — detailed procedure

**Post-generation:** applied to the **final RGB reconstruction image**, not to the decoded brain embedding. Flow: brain → decoded latents → Stable Cascade → reconstruction → encode reconstruction with CLIP → compare.

**Per reconstruction sample** (one of 10 × 3 seeds):

1. Encode **ground-truth image** $I_{\text{GT}}$, **reconstruction** $I_{\text{recon}}$, and **distractor image** $I_{\text{dist}}$ (another imagery stimulus of the **same type**) with CLIP ViT-L/14 **output layer**.
2. L2-normalise all three embedding vectors.
3. Compute $\cos_{\text{GT}} = \cos(I_{\text{GT}}, I_{\text{recon}})$ and $\cos_{\text{dist}} = \cos(I_{\text{dist}}, I_{\text{recon}})$.
4. **Binary success:** $1$ if $\cos_{\text{GT}} > \cos_{\text{dist}}$, else $0$.

**Reported CLIP 2WC score** = **fraction of successes** (mean of binary outcomes), range **[0, 1]** — often written as a **percentage** (e.g. 0.65 → 65%). This is **not** the size of the cosine gap and **not** “how much greater” the GT cosine is; it is only whether GT wins the pairwise comparison.

Average over 10 reconstructions × 3 seeds per subject × stimulus × condition.

**Reconstruction composite (for Option D):**

$$
R_{s,i,c} = \frac{1}{3}\left(z(\text{CLIP 2WC}) + z(\text{SSIM}) + z(\text{PixCorr})\right)
$$

computed over simple + complex stimuli only (12 per subject); z-scores computed across all applicable reconstruction cells for each metric separately.

**Conceptual stimuli (resolves open question #7):** Excluded from image-based reconstruction metrics. Report separately:

- Text cosine similarity (decoded vs concept prompt embedding).
- Text top-1 retrieval (k=1, N=50) against concept prompts of other conceptual stimuli.
- Text embedding 2AFC (as A4).

---

### C. MIRAGE component handling during ablation (resolves open question #3)

| Component                      | Image-only                | Text-only               | Combined         | Notes                                        |
| ------------------------------ | ------------------------- | ----------------------- | ---------------- | -------------------------------------------- |
| VDVAE ridge + decoder          | **On**                    | **On**                  | **On**           | Low-level path fixed                         |
| Image CLS ridge (768-d)        | **On**                    | **Off** (not trained)   | **On**           |                                              |
| Text ridge (77×1280)           | **Off** (not trained)     | **On**                  | **On**           |                                              |
| Retrieval hidden-layer ridge   | **On**                    | **On**                  | **On**           | Fixed — documented confound                  |
| Stable Cascade image guidance  | **Decoded CLS**           | **Zero vector** (768-d) | **Decoded CLS**  | Zero = literal zeros, not dropped connection |
| Stable Cascade text guidance   | **Zero vector** (77×1280) | **Decoded text**        | **Decoded text** |                                              |
| img2img / filtered VDVAE image | **On**                    | **On**                  | **On**           | Unchanged                                    |
| Retrieval pool (16 candidates) | **On**                    | **On**                  | **On**           | Same seed schedule                           |
| Caption decoding (GiT)         | **On**                    | **On**                  | **On**           | Diagnostic output only                       |

**Training rule:** Each condition trains **only its active ridge heads**; inactive heads are not fit. VDVAE and retrieval heads are always trained identically across conditions.

---

### D. Caption pipeline (resolves open question #4)

| Phase                              | Caption source                                                                                                       |
| ---------------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| **Training** (text ridge targets)  | **Fixed** LLaVA v1.5-13B synthetic captions from MIRAGE release artifacts — **not regenerated**                      |
| **Imagery inference**              | Text latents from **brain-decoded** ridge output only — no ground-truth captions                                     |
| **Ablation interpretability note** | Text-only condition never uses GT captions at test time; training caption quality is held constant across conditions |

---

## Decision thresholds

_Procedure definitions: `docs/references/statistical-methods-reference.md`_

### Baseline reproduction gate (resolves open question #8)

Before ablation comparison, full MIRAGE (combined condition) must pass:

| Criterion                                              | Threshold                                                                      | Reference             |
| ------------------------------------------------------ | ------------------------------------------------------------------------------ | --------------------- |
| CLIP 2WC (imagery, simple+complex, mean over subjects) | Within **±0.05 absolute** of published MIRAGE Table 1                          | Kneeland et al., 2026 |
| SSIM                                                   | Within **±0.05 absolute**                                                      | Same                  |
| PixCorr                                                | Within **±0.05 absolute**                                                      | Same                  |
| Per-subject pass                                       | ≥ **3 of 4** subjects within ±0.05 per metric                                  | Robustness check      |
| Failure action                                         | Halt ablation; document environment delta; do not reinterpret ablation results |

_If published values are ambiguous in extracted tables, use MIRAGE repo evaluation script output on subjects 1,2,5,7 as ground truth reference._

### Primary H₀ (Option A) — statistical plan (resolves open question #10)

**Unit of analysis:** subject × stimulus cells (4 × 18 = 72 per condition).

**Omnibus test:**

- **Method:** Freedman–Lane permutation ANOVA on _D<sub>s,i,c</sub>_ with factor **condition** (3 levels), **blocking by subject** (4 blocks), **10 000** permutations.
- **H₀ rejection:** omnibus _p_ < **α = 0.05**.

**Pre-registered pairwise post-hocs** (only if omnibus rejected):

| Contrast          | Test                                                                      | Multiplicity correction                                       |
| ----------------- | ------------------------------------------------------------------------- | ------------------------------------------------------------- |
| Image vs text     | Subject-level paired permutation (mean _D_ over 18 stimuli), 10 000 perms | Holm–Bonferroni over 3 tests                                  |
| Image vs combined | Same                                                                      | α<sub>adj</sub> = 0.05/3, 0.05/2, 0.05 for ordered _p_-values |
| Text vs combined  | Same                                                                      |                                                               |

**Adjusted significance threshold for each post-hoc:** smallest _p_ < 0.0167, second < 0.025, third < 0.05.

**Secondary confirmatory:** Repeat omnibus + post-hocs on each of top-1 retrieval, cosine, and 2AFC individually (Holm correction applied **within each metric family** across the 3 pairwise contrasts).

### Secondary H₀ (Option D) — linkage analysis (resolves open question #9)

**Model** (stimulus-level, cluster-robust by subject):

$$
R_{s,i,c} = \beta_0 + \beta_1 D_{s,i,c} + \beta_2 \cdot \mathbb{1}[\text{image-only}] + \beta_3 \cdot \mathbb{1}[\text{text-only}] + \epsilon_{s,i,c}
$$

- Reference level: **combined**.
- **H₀:** β₂ = β₃ = 0 (no residual condition effect after controlling for decoder quality).
- **Test:** Wald χ² on (β₂, β₃) with **HC1 cluster-robust SE** (4 subject clusters).
- **H₀ rejection (compensation evidence):** _p_ < **0.05**.
- **Supplementary:** Partial _R²_ for condition dummies; subject-level leave-one-subject-out stability check.

### Exploratory Option C

- Report mean _D_ and _R_ by stimulus type (simple / complex / conceptual) × condition.
- **No multiplicity-adjusted hypothesis tests.** Descriptive rank plots and 95% bootstrap CIs only.
- Acknowledge **6 stimuli per type** — underpowered.

### Uncertainty quantification (resolves open question #6)

| Method                   | Application                                                               | Mandatory?                                                |
| ------------------------ | ------------------------------------------------------------------------- | --------------------------------------------------------- |
| **Bootstrap 95% CI**     | 1000 resamples; stratified by subject                                     | **Yes** — all tables                                      |
| **Multi-seed SD**        | Report SD across 3 diffusion seeds                                        | **Yes** — reconstruction metrics                          |
| **Permutation null**     | Primary omnibus + post-hocs                                               | **Yes**                                                   |
| **Permutation baseline** | Decoder metrics vs **label-shuffled** brain–stimulus pairing (1000 perms) | **Yes** — sanity check; expect _p_ < 0.05 for real signal |
| **Bayesian estimation**  | Optional appendix                                                         | No                                                        |

---

## Leakage controls

### Checklist (study-specific)

- [ ] NSD-Imagery imagery trials excluded from all ridge fitting, λ tuning, and normalisation
- [ ] shared1000 image IDs excluded from NSD training split (Setting A)
- [ ] Strict holdout images (Setting B) excluded per audit manifest before any fit
- [ ] λ selected on subjects 3,4,6,8 only — never on 1,2,5,7 test subjects
- [ ] Per-run z-scoring for NSD-Imagery computed **within run**, not using cross-run or test statistics
- [ ] PCA / dimensionality reduction (if any) fit on training subjects' perception data only
- [ ] Distractor pools (retrieval, 2AFC) drawn from **fixed catalogues** (shared1000 or within-type imagery list) — no test-trial statistics inform pool construction
- [ ] CLIP / Stable Cascade / VDVAE weights frozen — no fine-tuning on imagery
- [ ] Caption artifacts fixed at train time — no peeking at imagery-trial captions
- [ ] Test manifest hash recorded **before** first training run
- [ ] Stimulus overlap audit frozen before training
- [ ] Reproduction gate passed before ablation comparisons

### Known residual confounds (accepted)

1. **Retrieval head** always uses hidden-layer image embedding — not ablated.
2. **VDVAE path** active in all conditions — low-level structure partially shared.
3. **Conceptual stimuli** lack image GT — reconstruction metrics incomparable to simple/complex.

---

## Frozen test manifest spec

**File:** `manifests/nsd_imagery_test_manifest_v1.json`

**Must include (frozen before execution):**

```json
{
  "version": "1.0.0",
  "created": "ISO-8601",
  "hash_algorithm": "sha256",
  "subjects": [1, 2, 5, 7],
  "tuning_subjects": [3, 4, 6, 8],
  "imagery_stimuli": [
    {
      "stimulus_id": "simple_bar_0deg",
      "type": "simple",
      "letter_cue": "...",
      "coco_id": null,
      "overlap_label": "non-image",
      "strict_holdout": true
    }
    // ... all 18
  ],
  "train_exclusions": {
    "shared1000": true,
    "setting_b_semantic_threshold": 0.85
  },
  "conditions": ["image_only", "text_only", "combined"],
  "seeds": [42, 123, 456],
  "reconstructions_per_seed": 10,
  "retrieval_distractors": {
    "N": 50,
    "pool": "nsd_shared1000",
    "distractor_resamples": 100
  },
  "embedding_2afc": { "distractors_per_target": 5, "within_type": true },
  "metrics": { "top_k": [1, 5, 10], "primary_k": 1 }
}
```

**Audit file:** `manifests/stimulus_overlap_audit.json` — per-subject exact-match and semantic-neighbour lists.

**Change control:** Increment version + re-hash; trigger downstream flush.

---

## Analysis plan

### Phase 0 — Audit and manifest freeze

1. Run stimulus overlap audit; populate manifest.
2. Hash manifest; commit to repo before any model training.

### Phase 1 — MIRAGE reproduction (combined only)

1. Train combined condition on Setting A split.
2. Evaluate reconstruction metrics on imagery (simple + complex).
3. **Gate:** pass reproduction thresholds (§Decision thresholds) or halt.

### Phase 2 — Three-way ablation (Setting A, primary)

1. Train image-only, text-only, combined with fair λ tuning.
2. Compute decoder metrics (A) on all 18 imagery stimuli.
3. Generate reconstructions (30 per stimulus); compute metrics (B).
4. **Primary inference:** Option A omnibus + post-hocs on _D_.
5. **Secondary inference:** Option D regression on _R_ ~ _D_ + condition.
6. Report bootstrap CIs, permutation baselines, multi-seed SD.

### Phase 3 — Strict holdout (Setting B, secondary)

Repeat Phase 2 with expanded training exclusions. Same tests; clearly labelled secondary. Do not replace primary conclusions.

### Phase 4 — Exploratory Option C

Descriptive breakdowns by stimulus type; no confirmatory claims.

### Phase 5 — Extensions (if time; resolves open question #11)

**Priority order** (highest information gain per effort):

| Rank | Extension                                     | Rationale                                                                                               |
| ---- | --------------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| 1    | **VDVAE on/off**                              | MIRAGE identifies low-level module as major imagery structure source — directly tests decoding vs prior |
| 2    | **ROI masks** (early vs higher visual cortex) | Supervisor interest; tests where transfer signal lives                                                  |
| 3    | **MLP backbone**                              | Lower priority — MIRAGE already shows ridge > MLP for imagery; high effort, lower novelty               |

Extensions use **same frozen test manifest** and metrics; separate exploratory report section.

### Reporting structure

1. Reproduction table vs MIRAGE published values.
2. Decoder-quality table (3 conditions × 3 metrics × 4 subjects).
3. Reconstruction table (simple + complex).
4. Conceptual-only text-metric table.
5. Primary permutation ANOVA + post-hoc table.
6. Secondary linkage regression table.
7. Setting A vs Setting B comparison.
8. Overlap audit summary (seen / neighbour / held-out counts).

---

## Limitations

| Limitation                                | Impact                                                                   | Mitigation                                                                                 |
| ----------------------------------------- | ------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------ |
| **N = 4 subjects**                        | Low power for subject-level inference; dominant uncertainty source       | Stimulus-level mixed/permutation tests; bootstrap CIs; report all per-subject trajectories |
| **18 imagery stimuli (6/type)**           | Option C underpowered; volatile metrics                                  | Pre-register exploratory status; avoid over-interpretation                                 |
| **Conceptual stimuli lack image GT**      | Reconstruction metrics undefined                                         | Separate text-only metrics; exclude from _R_ composite                                     |
| **Retrieval + VDVAE confounds**           | Option D residual effects may reflect retrieval, not just Stable Cascade | Report retrieval-head diagnostics; discuss in limitations                                  |
| **Semantic-neighbour threshold (0.85)**   | May exclude/include borderline neighbours                                | Investigator-approved; sensitivity at 0.80, 0.90 retained                                |
| **Decoder metrics on imagery**            | GT = cued image, not subjective mental content                           | Acknowledged in NSD-Imagery discussion                                                     |
| **shared1000 distractor pool**            | Small-scene bias for simple stimuli retrieval                            | Within-type sensitivity analysis                                                           |
| **MIRAGE reproduction tolerance (±0.05)** | May be too loose/tight                                                   | Calibrate against repo script in Phase 1                                                   |

---

## Approval checklist

- [x] Data domains and split protocol approved
- [x] Stimulus overlap audit and Setting A / B definitions approved (semantic-neighbour threshold **0.85**; conceptual lemma holdout)
- [x] Metric definitions (k=1, N=50, 2AFC protocol, embedding layers) approved
- [x] MIRAGE ablation component table approved (zero-vector protocol)
- [x] Caption pipeline (fixed train, decoded inference) approved
- [x] λ fairness protocol approved
- [x] Reproduction gate thresholds approved
- [x] Primary omnibus + Holm post-hoc plan approved
- [x] Secondary linkage regression specification approved
- [x] Decoder-quality composite endpoint approved
- [x] Frozen manifest schema approved
- [x] Extension priority order approved (or amended)
- [x] Ready to invoke **`pipeline-definition`** (approved 2026-09-07; revisit with supervisor if needed)

---

## Key citations

| ID  | Citation                                         | Role in this document                                      |
| --- | ------------------------------------------------ | ---------------------------------------------------------- |
| [1] | Kneeland et al., NSD-Imagery, CVPR 2025          | Benchmark split, metrics, 2AFC distractor logic            |
| [2] | Kneeland et al., MIRAGE, PLoS Comput Biol 2026   | Platform, λ tuning, retrieval protocol, ablation numbering |
| [3] | Supervisor feedback, `docs/proposal/feedback.md` | OOD dual reporting, uncertainty reporting                  |
| [4] | Scotti et al., MindEye, NeurIPS 2023             | Latent retrieval metric precedent                          |
| [5] | `docs/references/statistical-methods-reference.md` | Procedure reference: z-scores, permutation tests, L2 norm, CLIP 2WC, Holm, Wald |

**Investigator-approved (2026-09-07):** semantic-neighbour threshold 0.85; Setting B conceptual lemma holdout; decoder-quality composite endpoint. Sensitivity analyses at 0.80/0.90 retained. Revisit with supervisor feedback if required.

---

## Traceability

| Design choice                        | Source                                 |
| ------------------------------------ | -------------------------------------- |
| Subjects 1,2,5,7 / tuning 3,4,6,8    | Proposal §4; MIRAGE §4.2.1             |
| Train perception → test imagery      | Proposal §4; hypothesis formulation    |
| Three latent conditions              | Proposal §1; registered H₀ Option A    |
| Decoder vs reconstruction separation | Proposal §2–3; supervisor feedback     |
| Top-k, cosine, 2AFC metrics          | Hypothesis formulation (approved)      |
| CLIP 2WC, SSIM, PixCorr              | Hypothesis formulation; MIRAGE Table 1 |
| 10 reconstructions × seeds           | MIRAGE; NSD-Imagery supplement         |
| shared1000 retrieval pool            | MIRAGE Fig Q                           |
| Option D linkage                     | Registered secondary H₀                |
