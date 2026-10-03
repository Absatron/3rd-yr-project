## Citation

- **Authors:** Kneeland R, Villanueva CKT, Chen T, Ojeda J, Khanna S, Xu J, et al.
- **Year:** 2026
- **Title:** MIRAGE: Robust multi-modal architectures translate fMRI-to-image models from vision to mental imagery
- **Venue:** PLOS Computational Biology
- **Link / DOI:** [https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1014263](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1014263)

---

## 1. Research question

What problem does this paper address? (1–3 sentences in your own words.)

The problem that no SOTA decoders performance across seen and imagined images were consistent or correlated, and that the attributes which allow a model to generalise are unknown, they aim to provide an analysis which answers the latter and a decoder that solves the former and as a result provide practical utility within this problem space.

---

## 2. Setup

Train on / test on, dataset, subjects, models, evaluation protocol.

| Item             | Detail                                                                                                                                                                                                                                                                                              |
| ---------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Train            | NSD (Natural Scenes Dataset)                                                                                                                                                                                                                                                                        |
| Test             | NSD-Imagery — imagery trials (18 stimuli) as primary; vision trials (12 stimuli, simple+complex) as secondary; NSD shared1000 vision test as supplementary                                                                                                                                          |
| Dataset          | NSD-Imagery                                                                                                                                                                                                                                                                                         |
| Subjects         | 1,2,5 and 7 (train)                                                                                                                                                                                                                                                                                 |
| Models / methods | MIRAGE                                                                                                                                                                                                                                                                                              |
| Metrics          | Averaged across 10 reconstructions - Low-level: Pix-Corr, SSIM, Alex(2), Alex(5); High-level: Incep, CLIP, Eff, SwAV; Brain Correlation: Early Vis, Higher Vis, Visual Cortex; Captions: ROUGE-L, METEOR, Sentence, CLIP-LHuman identification accuracy scores for each stimulus (500 human raters) |

---

## 3. Key finding — relevant to my project

**Headline (one sentence):** The single most important takeaway for _your_ proposal. If you only remembered one thing from this paper for your project, what would it be?

- A ridge-regression backbone with compact multimodal CLIP guidance generalises from NSD perception training to NSD-Imagery mental imagery, while heavier MLP-based decoders overfit and fail to transfer.

**Supporting points (optional bullets):** Other findings that shape your design, hypotheses, or evaluation. Use bullets here — not instead of the headline.

- Stable Cascades performance was better with image only guidance over text only guidance, but performed best with the combination of the two
- Reconstructions with minimal guidance (nearly pure VDVAE encoding) remained highly identifiable, while increasing guidance strength primarily enhanced image quality rather than semantic content
  - Low level module (VDVAE) provides much of the needed structure for accurate mental imagery reconstruction
  - High dimensional image embeddings can be decoded and used to guide a retrieval module to improve performance
- Longer synthetic captions boosted performance over short synthetic and COCO captions
- Smaller image embeddings and larger text embeddings provide the most robust guidance for mental reconstruction
- The MLP backbone and diffusion prior backbone (MindEye1, MindEye2) perform worse than MIRAGE ridge regression backbone
- Mental image reconstruction is heavily influenced by the prior of the NSD training set

---

## 4. Design choices I might reuse

Metrics, baselines, ablations, splits, evaluation protocol, statistical reporting.

Metrics: Low-level: Pix-Corr, SSIM, Alex(2), Alex(5); High-level: Incep, CLIP, Eff, SwAV; Brain Correlation: Early Vis, Higher Vis, Visual Cortex; Captions: ROUGE-L, METEOR, Sentence, CLIP-L

Baselines: MIRAGE

Ablations: image only guidance vs text only guidance vs combined

Splits: Train exclusively on NSD, test on NSD-imagery, hyperparameter tuning set on unselected NSD subjects (3,4,6,8)

Evaluation protocol: 10 reconstructions averaged; Brain Diffuser, MindEye1, MindEye2, iCNN as benchmark

Statistical reporting: metrics table

---

## 5. Gap / limitation

What does this paper **not** answer that your project could address?

MIRAGE reports guidance ablations (image / text / combined) mainly as a normalised metric average (Fig 4B), not as a full low/high metric table per condition. It does not evaluate decoded CLIP guidance embeddings before diffusion (retrieval, cosine, 2AFC) per condition — an evaluation step specified in my project to separate neural decoding from generative prior effects.

---

## 6. Open questions (optional)

Terms, methods, or claims you do not yet understand. Return here on Pass 3 or when implementing.

---

## Reading passes used

- [x] Pass 1 — screened (abstract, figures, conclusions)
- [x] Pass 2 — notes completed
- [ ] Pass 3 — methods / implementation depth
