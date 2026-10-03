Project Title: What Enables Perception-to-Imagery Generalization in fMRI Vision Decoders?

Background: Reconstructing visual experiences from human brain activity offers a unique way to understand cognitive representations. Decoding mental imagery remains significantly more challenging than visual perception due to lower signal-to-noise ratios (SNR) and the absence of stimulus-driven responses. The NSD-Imagery benchmark (Kneeland et al., CVPR 2025) shows that state-of-the-art seen-image decoders do not reliably generalise to mental imagery, and that decoder design—not generative capacity—largely determines cross-task performance. MIRAGE (Kneeland et al., PLoS Computational Biology 2026) achieves the best imagery results using a ridge-regression backbone with multi-modal CLIP guidance, but it remains unclear how much each latent target contributes to genuine cross-task decoding versus compensation by a frozen diffusion prior.

Description: The objective is to determine which latent representations best support perception-trained decoders when tested on mental imagery. We will use the NSD-Imagery dataset (7T fMRI, vision and imagery tasks) and the open-source MIRAGE pipeline as a fixed experimental platform, varying only the neural-to-latent mapping stage.

1. Baseline and Ablations: We will reproduce MIRAGE on NSD-Imagery (train on perception, test on imagery) with Stable Cascade held frozen throughout. We will then ablate the mapper's latent targets: (a) CLIP image embeddings only, (b) CLIP text embeddings only, and (c) combined image and text embeddings.

2. Decoder Evaluation: For each condition, we will evaluate predicted latent representations before image generation—using retrieval accuracy, cosine similarity, and two-alternative forced-choice (2AFC) identification—reported per subject and stimulus type (simple, complex, conceptual).

3. Reconstruction Evaluation: The same predicted latents will be passed through the frozen diffusion model. We will compare reconstruction metrics (CLIP 2WC, SSIM, PixCorr) against decoder-quality results to determine whether apparent generalisation gains reflect neural decoding or generative prior compensation.

4. Cross-Task Protocol: All models train exclusively on NSD perception trials and test on NSD-Imagery imagery trials. Preprocessing and hyperparameter selection use training data only. Where feasible, we will additionally test a stricter stimulus-level holdout excluding imagery targets from perception training.

5. Extensions (if time permits): We may extend the core study with additional ablations—backbone complexity (ridge regression vs. MLP), the VDVAE low-level structural module (on/off), or cortical ROI masks (early vs. higher visual cortex)—and quantify the perception-to-imagery performance gap per condition to identify which design choices most reduce cross-task transfer loss.

Deliverables:

1. A reproducible ablation codebase (forked from MIRAGE) with modular latent-target and evaluation configuration.

2. Quantitative analysis comparing decoder-quality and reconstruction metrics across ablation conditions, identifying which latent representations most reduce the perception-to-imagery gap.

3. A written report discussing findings and implications for mental imagery decoding system design.
