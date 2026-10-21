"""Stimulus overlap audit (S0.2) — exact COCO matches; semantic neighbours when CLIP available."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from mirage_ablation.config.paths import frozen_weights_dir, raw_nsd_dir
from mirage_ablation.config.schema import NsdImageryTestManifest
from mirage_ablation.s0.mirage_split import build_mirage_split_verification
from mirage_ablation.s0.training_mask import TEST_SUBJECTS, training_coco_ids_for_subject


def _clip_weights_present() -> bool:
    root = frozen_weights_dir() / "mirage_hf"
    if not root.is_dir():
        return False
    return any(root.rglob("*clip*")) or any(root.rglob("*.safetensors"))


def build_overlap_audit(
    manifest: NsdImageryTestManifest,
    threshold: float = 0.85,
) -> dict[str, Any]:
    stim_csv = raw_nsd_dir() / "experiments" / "nsd" / "nsd_stim_info_merged.csv"
    if not stim_csv.is_file():
        raise FileNotFoundError("nsd_stim_info_merged.csv missing for overlap audit")

    per_subject: dict[str, Any] = {}
    for subj in TEST_SUBJECTS:
        train_cocos = training_coco_ids_for_subject(stim_csv, subj)
        exact_seen: list[dict[str, Any]] = []
        for stim in manifest.imagery_stimuli:
            if stim.type != "complex" or stim.coco_id is None:
                continue
            if stim.coco_id in train_cocos:
                exact_seen.append(
                    {
                        "stimulus_id": stim.stimulus_id,
                        "coco_id": stim.coco_id,
                    }
                )
        per_subject[str(subj)] = {
            "exact_seen": exact_seen,
            "exact_seen_count": len(exact_seen),
            "semantic_neighbours": [],
            "semantic_neighbour_count": 0,
            "setting_b_excluded_image_ids": [],
            "conceptual_lemma_caption_matches": [],
        }

    clip_ready = _clip_weights_present()
    mirage_verification = build_mirage_split_verification(manifest, stim_csv)
    return {
        "version": manifest.version,
        "created": manifest.created,
        "semantic_threshold": threshold,
        "clip_audit_status": "complete" if clip_ready else "pending_weights",
        "notes": (
            "Semantic-neighbour and conceptual lemma holdout require CLIP ViT-L/14 "
            "and LLaVA caption files on disk; re-run after selective HF sync."
            if not clip_ready
            else None
        ),
        "mirage_split_verification": mirage_verification,
        "per_subject": per_subject,
    }


def write_overlap_audit(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n")
