# Statistical and Metric Methods — Quick Reference

Brief definitions for procedures used in this project. Full protocol: `experimental_strategies/2026-09-06-perception-imagery-latent-ablation-experimental-strategy.md`.

**Field justification summary:** see [§ Method justification](#method-justification) at the end.

---

## L2 normalisation

**What:** Scale a vector $\mathbf{v}$ to unit length:

$$
\hat{\mathbf{v}} = \frac{\mathbf{v}}{\|\mathbf{v}\|_2}, \quad \|\mathbf{v}\|_2 = \sqrt{\sum_i v_i^2}
$$

**Why:** After L2 normalisation, **cosine similarity** equals the dot product: $\cos(\mathbf{a}, \mathbf{b}) = \hat{\mathbf{a}} \cdot \hat{\mathbf{b}}$.

**Where used:** All CLIP embedding comparisons (decoder metrics and CLIP 2WC).

**Precedent:** Standard for CLIP and contrastive embedding spaces (Radford et al., 2021).

---

## Mean-pooling (text embeddings)

**What:** Yes — **mean-pooling is averaging.** CLIP text encoder outputs **77 token vectors**, each 1280-dimensional. Mean-pooling takes the **element-wise arithmetic mean** across those 77 vectors:

$$
\bar{\mathbf{t}} = \frac{1}{77}\sum_{k=1}^{77} \mathbf{t}_k \in \mathbb{R}^{1280}
$$

Each dimension of $\bar{\mathbf{t}}$ is the average of that dimension across all 77 tokens. There is no separate trick beyond averaging.

**Why:** Metrics (cosine, retrieval, 2AFC) need a **single vector** per trial. Stable Cascade still receives the full **77 × 1280** tensor at generation time.

**Precedent:** Common when a sequence of token embeddings must be collapsed to one vector for similarity scoring (sentence-embedding practice; MIRAGE uses unpooled 77×1280 for generation only).

---

## Z-score

**What:** Standardise a value relative to a reference distribution:

$$
z = \frac{x - \mu}{\sigma}
$$

where $\mu$ and $\sigma$ are the mean and standard deviation over a defined set of cells.

**Properties:** Unitless; mean ≈ 0, SD ≈ 1 over the reference set. **Not** a percentage. **Not** bounded to [0, 1]. Negative = below average; positive = above average.

**Where used:** Before combining metrics into decoder composite $D$ and reconstruction composite $R$.

**Precedent:** Standard way to put metrics on comparable scales before combining; composite weighting is a **project design choice** (document in Methods).

---

## Decoder-quality composite $D_{s,i,c}$

**What “composite” adds:** Combines three metrics (top-1 retrieval, cosine, 2AFC) into **one score** per subject $s$, stimulus $i$, condition $c$ so conditions can be compared in a single omnibus test.

**Steps:**

1. Compute raw metrics per cell (retrieval ∈ [0,1], cosine ∈ [−1,1], 2AFC ∈ [0,1]).
2. Z-score each metric separately over applicable cells (144 image-stream cells or 144 text-stream cells).
3. Stream composite = mean of three z-scores.
4. Final $D_{s,i,c}$:
   - **image-only:** image-stream composite only
   - **text-only:** text-stream composite only
   - **combined:** mean(image-stream composite, text-stream composite) on the **same 72 trials** — not an average of the image-only and text-only **conditions**

**Primary endpoint:** the omnibus permutation test uses **216** values of $D_{s,i,c}$ (4 subjects × 18 stimuli × 3 conditions).

**Z-reference pools (144 each):** $\mu$ and $\sigma$ for image-stream metrics are computed over 144 raw measurements (image-only + combined image branch). Text-stream metrics use a separate 144-cell reference (text-only + combined text branch). Each cell gets one z-score relative to the appropriate reference; combined does not introduce a third latent space.

**Reporting:** Composite $D$ for primary omnibus; individual metrics (retrieval, cosine, 2AFC) reported separately as secondary confirmatory (MIRAGE/MindEye convention). Composite may be demoted to supplementary if supervisor feedback prefers per-metric primary tests.

---

## Top-k retrieval — chance vs significance

| Quantity                        | Value             | Meaning                                                     |
| ------------------------------- | ----------------- | ----------------------------------------------------------- |
| **Chance accuracy (k=1, N=50)** | 1/51 ≈ **0.0196** | Expected accuracy if guessing randomly among 51 candidates  |
| **Significance threshold**      | **α = 0.05**      | Permutation-test _p_-value for omnibus ANOVA on $D_{s,i,c}$ |

Beating chance (e.g. accuracy = 0.10 > 0.0196) does **not** by itself mean “statistically significant.” Significance comes from **comparing conditions** via the permutation test.

**Precedent:** Top-k retrieval in CLIP space — MindEye (Scotti et al., 2023); distractor protocol — MIRAGE Fig Q (Kneeland et al., 2026).

---

## Distractor resampling (retrieval)

**What:** For each stimulus, draw **100 different random sets** of N = 50 distractors from shared1000; compute top-1 accuracy each time; report the **mean** (and 95% CI across draws).

**Not:** Subject-level bootstrap. This only averages over distractor-set noise.

**Precedent:** MIRAGE Fig Q (Kneeland et al., 2026).

---

## CLIP 2WC (two-way comparison)

**Stage:** **Post-generation** — on the reconstructed **RGB image**, not the decoded latent.

**Per sample:**

1. Encode GT image, reconstruction, and distractor image with CLIP ViT-L/14 output layer.
2. Success if $\cos(\text{GT}, \text{recon}) > \cos(\text{distractor}, \text{recon})$ → binary **1** or **0**.
3. **Score** = fraction of successes in [0, 1] (reportable as %).

**Not:** The cosine gap magnitude. **Not:** A z-score. Only whether GT wins the pairwise comparison.

**Precedent:** NSD-Imagery Table 1 and supplement (Kneeland et al., CVPR 2025); MIRAGE Table 1 (Kneeland et al., 2026).

---

## Omnibus test

**What:** One overall test before pairwise comparisons: “Do the three conditions differ **at all** on $D_{s,i,c}$?”

**If** omnibus _p_ ≥ 0.05 → do not claim pairwise differences (or treat post-hocs as exploratory only).

**Precedent:** Standard analysis hierarchy in multi-condition experiments.

---

## Permutation test

**What:** Build a null distribution by shuffling data many times (**10 000** here) without assuming normality.

**p-value:** Fraction of permutations where the null statistic is at least as extreme as the observed statistic.

**Used for:** Primary omnibus and pairwise post-hocs on $D_{s,i,c}$.

**Precedent:** Widely used in neuroimaging with small subject N (Winkler et al., 2014, _NeuroImage_).

---

## Freedman–Lane permutation ANOVA

**What:** A permutation method for **repeated-measures** designs (same subjects in all three conditions).

**Blocking by subject:** Each of the 4 subjects contributes 18 imagery stimuli × 3 conditions.

**Freedman–Lane:** Permutes **residuals** (not raw scores) to preserve subject structure while testing the condition effect.

**Reference:** Freedman & Lane (1983); applied routinely in neuroimaging permutation inference.

---

## Holm–Bonferroni correction

**What:** Adjusts α when running **multiple pairwise tests** (3 contrasts: image vs text, image vs combined, text vs combined).

| Rank of p-value | Reject if p <       |
| --------------- | ------------------- |
| 1 (smallest)    | 0.05/3 = **0.0167** |
| 2               | 0.05/2 = **0.025**  |
| 3               | **0.05**            |

**Why:** Reduces false positives from multiple comparisons.

**Reference:** Holm (1979); standard in confirmatory science.

---

## Wald χ² test (secondary Option D)

**Model:**

$$
R_{s,i,c} = \beta_0 + \beta_1 D_{s,i,c} + \beta_2 \cdot \mathbb{1}[\text{image-only}] + \beta_3 \cdot \mathbb{1}[\text{text-only}] + \epsilon_{s,i,c}
$$

(reference level: **combined**)

**H₀:** $\beta_2 = \beta_3 = 0$ — no residual condition effect on reconstruction after controlling for decoder quality $D$.

**Wald χ²:** Joint test whether both condition dummies are zero.

**HC1 cluster-robust SE:** Standard errors that allow correlation among trials from the same subject (cluster = subject; only **4** clusters — interpret cautiously).

**Reject H₀ if:** _p_ < 0.05 → reconstruction differences persist beyond latent decoding → evidence for generative compensation.

**Precedent:** Standard regression / mediation-style framing; **operationalisation is project-specific** (supervisor-requested latent vs reconstruction separation).

---

## ViT hidden layer: 257 × 1024

CLIP ViT-L/14 hidden layer outputs **257 tokens** per image:

- **1** CLS token
- **256** patch tokens (14×14 patches)

MIRAGE flattens **257 × 1024** for the retrieval head. Do **not** use 256 × 1024.

**Precedent:** MIRAGE Fig 6 (Kneeland et al., 2026).

---

## Method justification

Methods fall into three tiers. Your report should cite **Tier 1** directly; acknowledge **Tier 2** as design choices with rationale; note limitations of **Tier 3**.

### Tier 1 — Field-standard (cite foundational / benchmark papers)

| Method                              | Why it is accepted                          | Primary citation                                                     |
| ----------------------------------- | ------------------------------------------- | -------------------------------------------------------------------- |
| **Cosine similarity** in CLIP space | Default metric for CLIP embeddings          | Radford et al. (2021); MindEye (Scotti et al., 2023)                 |
| **Top-k retrieval**                 | Standard fMRI→CLIP decoding evaluation      | MindEye; MIRAGE Fig Q                                                |
| **Embedding 2AFC**                  | Binary forced-choice in embedding space     | NSD-Imagery supplement; MindEye-style benchmarks                     |
| **CLIP 2WC, SSIM, PixCorr**         | NSD-Imagery / MIRAGE reconstruction battery | Kneeland et al. (CVPR 2025); Kneeland et al. (PLoS Comput Biol 2026) |
| **L2 normalisation**                | Required for cosine = dot product in CLIP   | Radford et al. (2021)                                                |
| **Train perception → test imagery** | NSD-Imagery cross-task protocol             | NSD-Imagery; MIRAGE                                                  |
| **α = 0.05**                        | Conventional significance level             | Universal convention                                                 |

### Tier 2 — Sound practice, project-specific operationalisation (justify in Methods)

| Method                                                                              | Rationale                                                                                                        |
| ----------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| **Z-score before composite**                                                        | Retrieval, cosine, and 2AFC live on different scales; z-scoring puts them on comparable footing before averaging |
| **Equal-weight composite** ($\frac{1}{3}$ per metric; 50/50 image/text in combined) | Simple, symmetric summary for omnibus test; pre-registered before results                                        |
| **Freedman–Lane permutation ANOVA**                                                 | Appropriate for repeated measures with **N = 4 subjects** where normality assumptions are weak                   |
| **Holm–Bonferroni**                                                                 | Conservative control for 3 pre-registered pairwise contrasts                                                     |
| **100 distractor resamples**                                                        | Matches MIRAGE Fig Q; stabilises retrieval estimates                                                             |
| **Mean-pooling text to 1280-d**                                                     | Metrics need one vector; generation still uses 77×1280                                                           |
| **Option D regression**                                                             | Directly tests supervisor-requested “latent vs reconstruction” separation                                        |

### Tier 3 — Acknowledge limitations in Discussion

| Issue                                   | Note                                                                                          |
| --------------------------------------- | --------------------------------------------------------------------------------------------- |
| **N = 4 subjects**                      | Low power; stimulus-level permutation helps but inference is fragile                          |
| **4 subject clusters for Wald test**    | Cluster-robust SE with 4 clusters is approximate — treat Option D as supportive               |
| **Composite is not in MIRAGE verbatim** | Novel summary for ablation comparison; individual metrics reported separately as confirmatory |

**Bottom line:** You do **not** need a novel statistical invention. Decoder and reconstruction **metrics** trace to NSD-Imagery, MIRAGE, and MindEye. **Inference** (permutation + Holm) follows neuroimaging best practice for small N. The **composite endpoint** is your pre-registered way to combine those established metrics — state that explicitly in Methods.

---

## Further reading

| Topic                            | Reference                                                         |
| -------------------------------- | ----------------------------------------------------------------- |
| Permutation tests (neuroimaging) | Winkler et al. (2014), _NeuroImage_                               |
| Holm correction                  | Holm (1979), _Scandinavian Journal of Statistics_                 |
| Freedman–Lane                    | Freedman & Lane (1983)                                            |
| CLIP embeddings                  | Radford et al. (2021), ICML                                       |
| fMRI decoding metrics            | Scotti et al. (2023), MindEye, NeurIPS                            |
| Benchmark protocol               | Kneeland et al. (2025) NSD-Imagery; Kneeland et al. (2026) MIRAGE |
