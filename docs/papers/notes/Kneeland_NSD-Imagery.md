## Citation

- **Authors:** Reese Kneeland, Paul S. Scotti, Ghislain St-Yves, Jesse Breedlove, Kendrick Kay, Thomas Naselaris
- **Year:** 2025
- **Title:** NSD-Imagery: A Benchmark Dataset for Extending fMRI Vision Decoding Methods to Mental Imagery
- **Venue:** CVPR 2025
- **Link / DOI:** [https://openaccess.thecvf.com/content/CVPR2025/papers/Kneeland_NSD-Imagery_A_Benchmark_Dataset_for_Extending_fMRI_Vision_Decoding_Methods_CVPR_2025_paper.pdf](https://openaccess.thecvf.com/content/CVPR2025/papers/Kneeland_NSD-Imagery_A_Benchmark_Dataset_for_Extending_fMRI_Vision_Decoding_Methods_CVPR_2025_paper.pdf)

---

## 1. Research question

What problem does this paper address? (1–3 sentences in your own words.)

The problem of decoding mental states from brain activity by testing whether recent methods for decoding seen images generalise to imagery and how the complexity of the imagined target stimuli might limit the quality of the reconstructed mental images

---

## 2. Setup

Train on / test on, dataset, subjects, models, evaluation protocol.

| Item             | Detail                                                                                                                                                                                                                                                 |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Train            | NSD visual perception trials                                                                                                                                                                                                                           |
| Test             | NSD-Imagery vision trials (12 stimuli) and imagery trials (18 stimuli) — cross-session, cross-task                                                                                                                                                     |
| Dataset          | NSD-imagery                                                                                                                                                                                                                                            |
| Subjects         | All 8 collected NSD-Imagery data; decoder benchmarks trained/evaluated on subjects 1, 2, 5, 7                                                                                                                                                          |
| Models / methods | MindEye1, Brain Diffuser, iCNN, MindEye2, Takagi et al                                                                                                                                                                                                 |
| Metrics          | Averaged across 10 reconstructions - Low-level: Pix-Corr, SSIM, Alex(2), Alex(5); High-level: Incep, CLIP, Eff, SwAV; Brain Correlation: Early Vis, Higher Vis, Visual CortexHuman identification accuracy scores for each stimulus (500 human raters) |

---

## 3. Key finding — relevant to my project

**Headline (one sentence):** The single most important takeaway for _your_ proposal. If you only remembered one thing from this paper for your project, what would it be?

- Vision decoding performance does not predict imagery decoding performance across methods — e.g. MindEye2 is near-chance on imagery despite strong vision results — suggesting architecture matters more than raw vision SOTA

**Supporting points (optional bullets):** Other findings that shape your design, hypotheses, or evaluation. Use bullets here — not instead of the headline.

- Decoding performance may be influenced by the consistency of training and test distributions and the priors more than any other decoding challenges
- Specific stimuli that reconstruct well for vision tend to also reconstruct well for imagery
- Brain correlation scores in the early cortex drop steeper than correlation scores in the higher visual cortex (vision to imagery)

---

## 4. Design choices I might reuse

Metrics, baselines, ablations, splits, evaluation protocol, statistical reporting.

Metrics - Low level metrics: PixCorr, SSIM; High level metrics: 2WC of layers; Distance metrics: Effnet-B SwAV, Brain Correlation Scores

Splits: train on NSD, test on NSD-imagery

Evalutation protocol: NSD-imagery benchmark

Statistical reporting: Table 1 structure: imagery / vision / shared1000 comparison blocks

---

## 5. Gap / limitation

What does this paper **not** answer that your project could address?

- No ablation of CLIP image vs text vs combined under a fixed protocol
- No latent-space evaluation before generation
- No strict stimulus-level holdout analysis

---

## 6. Open questions (optional)

Terms, methods, or claims you do not yet understand. Return here on Pass 3 or when implementing.

---

## Reading passes used

- [x] Pass 1 — screened (abstract, figures, conclusions)
- [x] Pass 2 — notes completed
- [ ] Pass 3 — methods / implementation depth
