"""Assemble the 18-stimulus NSD-Imagery test catalogue from official metadata."""

from __future__ import annotations

import csv
import re
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

from mirage_ablation.config.paths import raw_nsd_dir, raw_nsd_imagery_dir
from mirage_ablation.config.schema import ImageryStimulus, NsdImageryTestManifest

_SET_TO_TYPE = {"A": "simple", "B": "complex", "C": "conceptual"}


def _cue_pair_xlsx_path() -> Path:
    candidates = [
        raw_nsd_imagery_dir()
        / "experiments"
        / "nsdimagery"
        / "cue_pair_list.xlsx",
        raw_nsd_imagery_dir() / "metadata" / "cue_pair_list.xlsx",
    ]
    for p in candidates:
        if p.is_file():
            return p
    raise FileNotFoundError(
        "cue_pair_list.xlsx not found under data/raw/nsd_imagery; "
        "run M0 AWS sync (nsddata/experiments/nsdimagery/) first."
    )


def _nsd_stim_info_csv() -> Path:
    p = raw_nsd_dir() / "experiments" / "nsd" / "nsd_stim_info_merged.csv"
    if not p.is_file():
        raise FileNotFoundError(
            "nsd_stim_info_merged.csv not found; sync nsddata/experiments/nsd/ first."
        )
    return p


def _read_xlsx_rows(path: Path) -> list[list[str]]:
    with zipfile.ZipFile(path) as z:
        shared = ET.fromstring(z.read("xl/sharedStrings.xml"))
        ns = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
        strings: list[str] = []
        for si in shared.findall("m:si", ns):
            t = si.find("m:t", ns)
            if t is not None:
                strings.append(t.text or "")
            else:
                strings.append("".join(n.text or "" for n in si.findall(".//m:t", ns)))
        sheet = ET.fromstring(z.read("xl/worksheets/sheet1.xml"))
        rows: list[list[str]] = []
        for row in sheet.findall(".//m:sheetData/m:row", ns):
            vals: list[str] = []
            for c in row.findall("m:c", ns):
                v = c.find("m:v", ns)
                if v is None:
                    vals.append("")
                    continue
                if c.get("t") == "s":
                    vals.append(strings[int(v.text)])
                else:
                    vals.append(v.text or "")
            rows.append(vals)
    return rows


def _load_nsd_id_maps(csv_path: Path) -> tuple[dict[str, str], dict[str, bool]]:
    nsd_to_coco: dict[str, str] = {}
    shared1000: dict[str, bool] = {}
    with csv_path.open(newline="") as f:
        for row in csv.DictReader(f):
            nsd_to_coco[row["nsdId"]] = row["cocoId"]
            shared1000[row["nsdId"]] = row.get("shared1000", "").lower() == "true"
    return nsd_to_coco, shared1000


def _simple_stimulus_id(target: str) -> str:
    if target.startswith("bar_"):
        deg = target.split("_")[1].replace(".0deg", "deg")
        return f"simple_bar_{deg}"
    if target.startswith("crs_"):
        deg = target.split("_")[1].replace(".0deg", "deg")
        return f"simple_cross_{deg}"
    raise ValueError(f"unrecognized simple target filename: {target}")


def _complex_ids(target: str, nsd_to_coco: dict[str, str]) -> tuple[int | None, int | None]:
    m = re.search(r"nsd(\d+)", target)
    if not m:
        return None, None
    nsd_id = int(m.group(1))
    coco_s = nsd_to_coco.get(str(nsd_id)) or nsd_to_coco.get(str(nsd_id).zfill(5))
    if coco_s is None or coco_s == "":
        return nsd_id, None
    return nsd_id, int(coco_s)


def _conceptual_stimulus_id(label: str) -> str:
    safe = re.sub(r"[^a-z0-9]+", "_", label.strip().lower())
    return f"conceptual_{safe}"


def build_test_manifest() -> NsdImageryTestManifest:
    cue_path = _cue_pair_xlsx_path()
    stim_csv = _nsd_stim_info_csv()
    nsd_to_coco, shared_flags = _load_nsd_id_maps(stim_csv)

    rows = _read_xlsx_rows(cue_path)
    if not rows or rows[0][:3] != ["stim_set", "target", "cue"]:
        raise ValueError(f"unexpected cue_pair_list header: {rows[0] if rows else 'empty'}")

    stimuli: list[ImageryStimulus] = []
    for stim_set, target, cue in rows[1:]:
        stype = _SET_TO_TYPE.get(stim_set)
        if stype is None:
            continue
        if stype == "simple":
            sid = _simple_stimulus_id(target)
            stimuli.append(
                ImageryStimulus(
                    stimulus_id=sid,
                    type="simple",
                    letter_cue=cue,
                    coco_id=None,
                    nsd_id=None,
                    target_label=target,
                    overlap_label="non-image",
                    strict_holdout=True,
                )
            )
        elif stype == "complex":
            nsd_id, coco_id = _complex_ids(target, nsd_to_coco)
            sid = f"complex_nsd{nsd_id:05d}" if nsd_id is not None else f"complex_{target}"
            if nsd_id == 0 or "nsd00000" in target:
                overlap = "artwork"
            elif target.startswith("shared"):
                overlap = "shared1000"
            elif nsd_id is not None and shared_flags.get(str(nsd_id)):
                overlap = "shared1000"
            else:
                overlap = "strict-held-out"
            stimuli.append(
                ImageryStimulus(
                    stimulus_id=sid,
                    type="complex",
                    letter_cue=cue,
                    coco_id=coco_id,
                    nsd_id=nsd_id,
                    target_label=target,
                    overlap_label=overlap,
                    strict_holdout=True,
                )
            )
        else:
            sid = _conceptual_stimulus_id(target)
            stimuli.append(
                ImageryStimulus(
                    stimulus_id=sid,
                    type="conceptual",
                    letter_cue=cue,
                    coco_id=None,
                    nsd_id=None,
                    target_label=target,
                    overlap_label="non-image",
                    strict_holdout=True,
                )
            )

    stimuli.sort(key=lambda s: (s.type, s.stimulus_id))
    data = raw_nsd_imagery_dir().parent.parent
    return NsdImageryTestManifest(
        created=NsdImageryTestManifest.now_iso(),
        source_files=[
            str(cue_path.relative_to(data)),
            str(stim_csv.relative_to(data)),
        ],
        imagery_stimuli=stimuli,
    )
