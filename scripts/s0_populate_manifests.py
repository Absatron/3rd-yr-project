#!/usr/bin/env python3
"""S0 manifest population CLI (shared Track A / Track B)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from mirage_ablation.config.paths import manifests_dir, repo_root
from mirage_ablation.s0.catalogue import build_test_manifest
from mirage_ablation.s0.catalogues import freeze_distractor_catalogues
from mirage_ablation.s0.overlap_audit import build_overlap_audit, write_overlap_audit
from mirage_ablation.s0.weights_manifest import write_weights_manifest


def main() -> int:
    parser = argparse.ArgumentParser(description="Populate S0 manifests and catalogues.")
    parser.add_argument(
        "--output",
        type=Path,
        help="Output JSON path (test manifest or overlap audit).",
    )
    parser.add_argument("--audit", action="store_true", help="Run overlap audit (S0.2).")
    parser.add_argument(
        "--threshold",
        type=float,
        default=0.85,
        help="Semantic neighbour cosine threshold (S0.2).",
    )
    parser.add_argument(
        "--freeze-catalogues",
        action="store_true",
        help="Write distractor catalogue skeletons (S0.3).",
    )
    parser.add_argument(
        "--weights-manifest",
        action="store_true",
        help="Write model_weights_manifest.json from on-disk frozen weights (S0.4).",
    )
    args = parser.parse_args()

    if args.freeze_catalogues:
        from mirage_ablation.config.schema import NsdImageryTestManifest

        manifest_path = manifests_dir() / "nsd_imagery_test_manifest_v1.json"
        if not manifest_path.is_file():
            print("error: run default manifest population first", file=sys.stderr)
            return 1
        manifest = NsdImageryTestManifest.model_validate_json(manifest_path.read_text())
        paths = freeze_distractor_catalogues(manifest)
        print("wrote catalogues:", ", ".join(str(p) for p in paths.values()))
        return 0

    if args.weights_manifest:
        out = manifests_dir() / "model_weights_manifest.json"
        payload = write_weights_manifest(out)
        print(f"wrote {out} ({payload['status']}, {len(payload['artifacts'])} files)")
        return 0

    if args.audit:
        manifest_path = manifests_dir() / "nsd_imagery_test_manifest_v1.json"
        if not manifest_path.is_file():
            manifest = build_test_manifest()
        else:
            from mirage_ablation.config.schema import NsdImageryTestManifest

            manifest = NsdImageryTestManifest.model_validate_json(manifest_path.read_text())
        audit = build_overlap_audit(manifest, threshold=args.threshold)
        out = args.output or manifests_dir() / "stimulus_overlap_audit.json"
        write_overlap_audit(out, audit)
        print(f"wrote {out} (clip_audit_status={audit['clip_audit_status']})")
        return 0

    manifest = build_test_manifest()
    out = args.output or manifests_dir() / "nsd_imagery_test_manifest_v1.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(manifest.model_dump_json(indent=2) + "\n")
    print(f"wrote {out} with {len(manifest.imagery_stimuli)} stimuli")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
