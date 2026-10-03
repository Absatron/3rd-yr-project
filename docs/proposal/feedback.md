Hi James,
Thank you for sharing the proposal. there has been substantial recent progress in this area, so I suggest refining the project in the following four ways.

Clarify the novelty relative to recent work.
A particularly relevant paper is MIRAGE: Robust Multi-modal Architectures Translate fMRI-to-Image Models from Vision to Mental Imagery, published in PLOS Computational Biology in 2026. Its central setup is very close to your proposal: it trains linear fMRI-to-feature mappings on visual-perception data and uses decoded image and text features to reconstruct mental imagery through a diffusion model. You should therefore explain clearly what your project will contribute beyond reproducing existing results such as MIRAGE. A feasible contribution could be a controlled study of which latent representations, cortical regions and feature dimensions transfer best from perception to imagery.

Paper: https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1014263
Code: https://github.com/MedARC-AI/MIRAGE

You can also read the original CVPR 2025 NSD-Imagery paper carefully, particularly its comparisons between linear and more complex decoding architectures:

https://openaccess.thecvf.com/content/CVPR2025/html/Kneeland_NSD-Imagery_A_Benchmark_Dataset_for_Extending_fMRI_Vision_Decoding_Methods_CVPR_2025_paper.html

Define the OOD setting more precisely.
Training on perception and testing on imagery demonstrates cross-task generalisation, but it does not necessarily demonstrate generalisation to unseen visual content. Some NSD-Imagery targets are also drawn from the original NSD stimulus set. If you want to claim stronger OOD generalisation, you should report two settings separately: perception-to-imagery transfer when the target image has appeared during perception training, and a stricter setting in which all imagery target images—and preferably close semantic neighbours—are removed from the training data. PCA, feature normalisation and hyperparameter selection must also use training data only.

Use a small but informative set of baselines and ablations.
Begin with a reproducible baseline rather than introducing a new complex architecture immediately. Compare fMRI mappings to:
(a) CLIP image embeddings,
(b) CLIP text embeddings, and
(c) combined image and text embeddings.

You can first keep the diffusion model frozen so that the experiment measures neural-to-latent alignment rather than the capacity of a fine-tuned generator.

Separate neural decoding quality from image-generation quality.
A diffusion model can produce plausible images even when the decoded brain representation is weak. Evaluate the predicted latent representations before generating images, using retrieval accuracy, cosine similarity and two-alternative identification. Then evaluate the reconstructions using complementary semantic and structural metrics. Results should be reported per subject and stimulus type, with permutation baselines, repeated random seeds and bootstrap confidence intervals. This will make it clearer whether improvements come from genuine imagery decoding or from the generative prior.

Overall, the project remains feasible, but the current description is too close to recently published work. I suggest repositioning it as a careful and reproducible investigation of what enables perception-trained neural decoders to generalise to mental imagery, rather than simply building another fMRI-to-diffusion pipeline.

Best,
Jingyuan
