"""Cross-check Setting A overlap audit against MedARC-AI/MIRAGE ``load_nsd`` training mask."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from mirage_ablation.config.paths import raw_nsd_dir
from mirage_ablation.config.schema import NsdImageryTestManifest
from mirage_ablation.s0.training_mask import (
    TEST_SUBJECTS,
    mirage_train_nsd_ids_for_subject,
    training_coco_ids_for_subject,
)

MIRAGE_UTILS_REF = (
    "https://github.com/MedARC-AI/MIRAGE/blob/main/src/utils.py"
    " (function load_nsd: subject saw image and stim_descriptions['shared1000'] == False)"
)


def build_mirage_split_verification(
    manifest: NsdImageryTestManifest,
    stim_csv: Path | None = None,
) -> dict[str, Any]:
    """
    For each complex imagery target, compare audit ``exact_seen`` with MIRAGE ``load_nsd``.

    Non-zero ``exact_seen`` under Setting A is expected when the imagery scene's ``nsd_id``
    appears on a CSV row with ``shared1000=False`` (imagery ``overlap_label`` is not the
    same as that column).
    """
    stim_csv = stim_csv or raw_nsd_dir() / "experiments" / "nsd" / "nsd_stim_info_merged.csv"
    if not stim_csv.is_file():
        raise FileNotFoundError(f"nsd_stim_info_merged.csv missing: {stim_csv}")

    complex_stimuli = [s for s in manifest.imagery_stimuli if s.type == "complex"]
    per_subject: dict[str, Any] = {}
    all_agree = True

    for subj in TEST_SUBJECTS:
        train_cocos = training_coco_ids_for_subject(stim_csv, subj)
        train_nsd = mirage_train_nsd_ids_for_subject(stim_csv, subj)
        comparisons: list[dict[str, Any]] = []
        for stim in complex_stimuli:
            if stim.coco_id is None or stim.nsd_id is None:
                continue
            audit_exact = stim.coco_id in train_cocos
            mirage_nsd_in_train = stim.nsd_id in train_nsd
            agree = audit_exact == mirage_nsd_in_train
            if not agree:
                all_agree = False
            comparisons.append(
                {
                    "stimulus_id": stim.stimulus_id,
                    "nsd_id": stim.nsd_id,
                    "coco_id": stim.coco_id,
                    "overlap_label": stim.overlap_label,
                    "audit_exact_seen": audit_exact,
                    "mirage_nsd_in_train": mirage_nsd_in_train,
                    "agreement": agree,
                }
            )
        per_subject[str(subj)] = {
            "comparisons": comparisons,
            "all_agreements": all(c["agreement"] for c in comparisons),
        }

    rel_stim = "raw/nsd/experiments/nsd/nsd_stim_info_merged.csv"
    return {
        "mirage_reference": MIRAGE_UTILS_REF,
        "stim_csv": rel_stim,
        "notes": (
            "Setting A excludes rows with shared1000=True in nsd_stim_info_merged.csv "
            "(1000 images), matching MIRAGE load_nsd. NSD-Imagery complex scenes labelled "
            "shared1000 in the test manifest may still have shared1000=False in that CSV; "
            "exact_seen>0 can match MIRAGE and is not a reproduction blocker. "
            "Use Setting B to remove exact_seen targets for strict holdout."
        ),
        "all_subjects_agree": all_agree,
        "per_subject": per_subject,
    }
