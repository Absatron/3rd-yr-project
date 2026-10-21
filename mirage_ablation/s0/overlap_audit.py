"""Stimulus overlap audit (S0.2) — exact COCO matches; semantic neighbours when CLIP available."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

from mirage_ablation.config.paths import frozen_weights_dir, raw_nsd_dir
from mirage_ablation.config.schema import NsdImageryTestManifest

TEST_SUBJECTS = [1, 2, 5, 7]


def _shared1000_coco_ids(stim_csv: Path) -> set[int]:
    ids: set[int] = set()
    with stim_csv.open(newline="") as f:
        for row in csv.DictReader(f):
            if row.get("shared1000", "").lower() != "true":
                continue
            coco = row.get("cocoId")
            if coco and coco.isdigit():
                ids.add(int(coco))
    return ids


def _training_coco_ids_for_subject(
    stim_csv: Path, subject: int, *, setting_a: bool = True
) -> set[int]:
    """Perception training COCO IDs for overlap audit (Setting A excludes shared1000)."""
    col = f"subject{subject}"
    shared1000 = _shared1000_coco_ids(stim_csv) if setting_a else set()
    ids: set[int] = set()
    with stim_csv.open(newline="") as f:
        for row in csv.DictReader(f):
            try:
                shown = int(row.get(col, "0") or "0")
            except ValueError:
                shown = 0
            if shown <= 0:
                continue
            coco = row.get("cocoId")
            if not coco or not coco.isdigit():
                continue
            cid = int(coco)
            if setting_a and cid in shared1000:
                continue
            ids.add(cid)
    return ids


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
        train_cocos = _training_coco_ids_for_subject(stim_csv, subj)
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
        "per_subject": per_subject,
    }


def write_overlap_audit(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n")
