"""Setting A perception training masks (audit + MIRAGE load_nsd alignment)."""

from __future__ import annotations

import csv
from pathlib import Path

TEST_SUBJECTS = [1, 2, 5, 7]


def shared1000_coco_ids(stim_csv: Path) -> set[int]:
    ids: set[int] = set()
    with stim_csv.open(newline="") as f:
        for row in csv.DictReader(f):
            if row.get("shared1000", "").lower() != "true":
                continue
            coco = row.get("cocoId")
            if coco and coco.isdigit():
                ids.add(int(coco))
    return ids


def training_coco_ids_for_subject(
    stim_csv: Path, subject: int, *, setting_a: bool = True
) -> set[int]:
    """Perception training COCO IDs for overlap audit (Setting A excludes shared1000 rows)."""
    col = f"subject{subject}"
    shared1000 = shared1000_coco_ids(stim_csv) if setting_a else set()
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


def mirage_train_nsd_ids_for_subject(stim_csv: Path, subject: int) -> set[int]:
    """NSD image IDs used in MIRAGE ridge training for one subject."""
    col = f"subject{subject}"
    ids: set[int] = set()
    with stim_csv.open(newline="") as f:
        for row in csv.DictReader(f):
            if row.get("shared1000", "").lower() == "true":
                continue
            try:
                shown = int(row.get(col, "0") or "0")
            except ValueError:
                shown = 0
            if shown == 0:
                continue
            nsd = row.get("nsdId")
            if nsd and nsd.isdigit():
                ids.add(int(nsd))
    return ids
