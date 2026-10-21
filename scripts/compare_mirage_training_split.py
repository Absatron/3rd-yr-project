#!/usr/bin/env python3
"""Compare Setting A exact_seen audit with MIRAGE load_nsd training mask (HG-0 helper)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from mirage_ablation.config.paths import manifests_dir
from mirage_ablation.config.schema import NsdImageryTestManifest
from mirage_ablation.s0.mirage_split import build_mirage_split_verification


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Verify overlap audit exact_seen against MedARC-AI/MIRAGE load_nsd."
    )
    parser.add_argument(
        "--manifest",
        type=Path,
        default=manifests_dir() / "nsd_imagery_test_manifest_v1.json",
        help="NSD-Imagery test manifest JSON.",
    )
    parser.add_argument(
        "--stim-csv",
        type=Path,
        default=None,
        help="Override path to nsd_stim_info_merged.csv (default: data/raw/.../nsd_stim_info_merged.csv).",
    )
    parser.add_argument(
        "--write-audit",
        type=Path,
        nargs="?",
        const=manifests_dir() / "stimulus_overlap_audit.json",
        help="Merge mirage_split_verification into this audit JSON (default: manifests/stimulus_overlap_audit.json).",
    )
    parser.add_argument(
        "--fail-on-mismatch",
        action="store_true",
        help="Exit 1 if any complex stimulus disagrees between audit and MIRAGE mask.",
    )
    args = parser.parse_args()

    if not args.manifest.is_file():
        print(f"error: manifest not found: {args.manifest}", file=sys.stderr)
        return 1

    manifest = NsdImageryTestManifest.model_validate_json(args.manifest.read_text())
    verification = build_mirage_split_verification(manifest, args.stim_csv)

    for subj, block in verification["per_subject"].items():
        mismatches = [c for c in block["comparisons"] if not c["agreement"]]
        exact_hits = [c for c in block["comparisons"] if c["audit_exact_seen"]]
        print(
            f"subject {subj}: mirage_audit_agree={block['all_agreements']} "
            f"exact_seen_complex={len(exact_hits)}"
        )
        for c in exact_hits:
            print(
                f"  {c['stimulus_id']} nsd={c['nsd_id']} coco={c['coco_id']} "
                f"(mirage_nsd_in_train={c['mirage_nsd_in_train']})"
            )
        for c in mismatches:
            print(
                f"  MISMATCH {c['stimulus_id']}: audit={c['audit_exact_seen']} "
                f"mirage={c['mirage_nsd_in_train']}",
                file=sys.stderr,
            )

    print(f"all_subjects_agree={verification['all_subjects_agree']}")

    if args.write_audit is not None:
        audit_path = args.write_audit
        if audit_path.is_file():
            audit = json.loads(audit_path.read_text())
        else:
            audit = {}
        audit["mirage_split_verification"] = verification
        audit_path.parent.mkdir(parents=True, exist_ok=True)
        audit_path.write_text(json.dumps(audit, indent=2) + "\n")
        print(f"updated {audit_path}")

    if args.fail_on_mismatch and not verification["all_subjects_agree"]:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
