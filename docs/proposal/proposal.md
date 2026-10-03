Project Title: Neuro-Diffusion: Cross-Decoding Mental Imagery from fMRI via Latent Diffusion Models

Background: Reconstructing visual experiences from human brain activity offers a unique way to understand cognitive representations. While visual perception decoding is heavily researched, decoding mental imagery remains significantly more challenging due to lower signal-to-noise ratios (SNR) and the absence of stimulus-driven responses. This project utilizes the recent NSD-Imagery benchmark to assess out-of-distribution (OOD) generalization. By aligning neural signals with the latent spaces of Generative AI, this project bridges biological cognition with artificial generation to decode what the mind's eye is imagining.

Description: The objective is to build a cross-decoding pipeline that reconstructs mental imagery from brain activity. We will utilize the NSD-Imagery dataset, which contains high-resolution 7T fMRI measurements of subjects performing both vision and mental imagery tasks.

The methodology focuses on "Latent Alignment" and OOD evaluation:

1. Feature Extraction: We will leverage a pre-trained Generative AI model's latent space (such as CLIP embeddings) to represent the semantic content of the visual stimuli.

2. The Mapper: We will train a lightweight linear neural network (e.g., Ridge Regression) to map fMRI voxels to the semantic latent space. Crucially, training will occur exclusively on visual perception tasks, while inference will be conducted on the held-out mental imagery tasks to test generalization.

3. Generation: The predicted latent representations from the mental imagery trials will guide a frozen Stable Diffusion prior to synthesize the imagined content.

Deliverables:

4. The Neuro-Diffusion Pipeline: A functional codebase handling fMRI data ingestion, cross-modal mapping, and HuggingFace Diffusers integration.

5. Reconstruction Evaluation: A comparative analysis highlighting the generalization gap between seen and imagined image reconstructions.

6. Quantitative Analysis: Evaluation of semantic similarity and structural fidelity across the cognitive gap.
