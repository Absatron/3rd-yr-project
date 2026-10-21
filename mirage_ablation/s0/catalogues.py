"""S0.3 distractor catalogue placeholders (full embeddings after shared1000 CLIP encode)."""

from __future__ import annotations

import json
from pathlib import Path

from mirage_ablation.config.paths import frozen_catalogues_dir
from mirage_ablation.config.schema import NsdImageryTestManifest


def freeze_distractor_catalogues(manifest: NsdImageryTestManifest) -> dict[str, Path]:
    out_dir = frozen_catalogues_dir()
    out_dir.mkdir(parents=True, exist_ok=True)

    within_type = {
        "version": manifest.version,
        "created": manifest.created,
        "N_pool": manifest.retrieval_distractors.N,
        "distractors_per_target": manifest.embedding_2afc.distractors_per_target,
        "within_type": manifest.embedding_2afc.within_type,
        "status": "skeleton",
        "notes": (
            "Populate candidate pools after shared1000_embeddings.npz is built in S3/S0 "
            "with frozen CLIP ViT-L/14; no test-trial statistics used (HC-11)."
        ),
        "by_type": {
            "simple": [s.stimulus_id for s in manifest.imagery_stimuli if s.type == "simple"],
            "complex": [s.stimulus_id for s in manifest.imagery_stimuli if s.type == "complex"],
            "conceptual": [
                s.stimulus_id for s in manifest.imagery_stimuli if s.type == "conceptual"
            ],
        },
    }
    within_path = out_dir / "within_type_imagery_list.json"
    within_path.write_text(json.dumps(within_type, indent=2) + "\n")

    npz_path = out_dir / "shared1000_embeddings.npz"
    outputs: dict[str, Path] = {"within_type_imagery_list.json": within_path}
    if npz_path.is_file() and npz_path.stat().st_size > 0:
        outputs["shared1000_embeddings.npz"] = npz_path
    return outputs
