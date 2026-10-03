# Papers

Reference library for fMRI vision decoding and mental imagery generalization. Markdown extractions live under `mds/` (from Marker); originals under `pdfs/`.

## Reading order

1. **NSD-Imagery (CVPR 2025)** — dataset, benchmark setup, and baseline cross-decoding results.
2. **MIRAGE (PLoS Comp Biol 2026)** — SOTA method built on those findings; architecture and ablations.

## Papers

| Paper | What it covers | Markdown | PDF |
|-------|----------------|----------|-----|
| **NSD-Imagery** — A benchmark dataset for extending fMRI vision decoding to mental imagery (Kneeland et al., CVPR 2025) | Releases NSD-Imagery benchmark; shows vision decoding performance does not reliably predict mental imagery performance; benchmarks MindEye1/2, Brain Diffuser, iCNN, Takagi et al. | [md](mds/Kneeland_NSD-Imagery_A_Benchmark_Dataset_for_Extending_fMRI_Vision_Decoding_Methods_CVPR_2025_paper/Kneeland_NSD-Imagery_A_Benchmark_Dataset_for_Extending_fMRI_Vision_Decoding_Methods_CVPR_2025_paper.md) | [pdf](pdfs/Kneeland_NSD-Imagery_A_Benchmark_Dataset_for_Extending_fMRI_Vision_Decoding_Methods_CVPR_2025_paper.pdf) |
| **MIRAGE** — Robust multi-modal architectures translate fMRI-to-image models from vision to mental imagery (Kneeland et al., PLoS Comp Biol 2026) | Linear backbone + multi-modal (text + image) features → diffusion; SOTA on NSD-Imagery; ablations on what enables vision→imagery generalization | [md](mds/journal.pcbi.1014263/journal.pcbi.1014263.md) | [pdf](pdfs/journal.pcbi.1014263.pdf) |

## Quick lookup

| Question | Start here |
|----------|------------|
| Dataset structure, stimulus types (simple / complex / conceptual), task design | NSD-Imagery §3 |
| Baseline model comparisons on imagery vs vision | NSD-Imagery §4 |
| Why MindEye2 fails on imagery but MIRAGE succeeds | MIRAGE §1, §2.3 (ablations) |
| MIRAGE architecture and training | MIRAGE §4.2 |
| Human rater experiments | Both papers (NSD-Imagery §4.5; MIRAGE §2.2) |
| Feature metrics (PixCorr, SSIM, AlexNet, CLIP, brain correlation, etc.) | MIRAGE Table 1; NSD-Imagery §4.4 |

## External links

- NSD-Imagery / NSD data: [naturalscenesdataset.org](https://naturalscenesdataset.org/)
- MIRAGE code: [github.com/MedARC-AI/MIRAGE](https://github.com/MedARC-AI/MIRAGE)
- MIRAGE DOI: [10.1371/journal.pcbi.1014263](https://doi.org/10.1371/journal.pcbi.1014263)
