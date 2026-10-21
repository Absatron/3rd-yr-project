#!/usr/bin/env python3
"""S0.5 — validate manifests and write SHA-256 sidecars."""

from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from mirage_ablation.config.paths import manifests_dir, repo_root
from mirage_ablation.config.schema import NsdImageryTestManifest

MANIFEST_FILES = (
    "nsd_imagery_test_manifest_v1.json",
    "stimulus_overlap_audit.json",
)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def write_hash_sidecar(json_path: Path) -> str:
    digest = sha256_file(json_path)
    sidecar = json_path.with_suffix(json_path.suffix + ".sha256")
    sidecar.write_text(f"{digest}  {json_path.name}\n")
    return digest


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--write-hashes",
        action="store_true",
        help="Write .sha256 sidecars for manifest JSON files.",
    )
    args = parser.parse_args()

    errors: list[str] = []
    test_path = manifests_dir() / "nsd_imagery_test_manifest_v1.json"
    if test_path.is_file():
        try:
            NsdImageryTestManifest.model_validate_json(test_path.read_text())
        except Exception as exc:
            errors.append(f"schema validation failed for {test_path}: {exc}")
    else:
        errors.append(f"missing {test_path}")

    audit_path = manifests_dir() / "stimulus_overlap_audit.json"
    if not audit_path.is_file():
        errors.append(f"missing {audit_path}")

    if errors:
        for e in errors:
            print(e, file=sys.stderr)
        return 1

    if args.write_hashes:
        for name in MANIFEST_FILES:
            p = manifests_dir() / name
            if p.is_file():
                digest = write_hash_sidecar(p)
                print(f"{p.name}: {digest}")

    print("verify: OK (hashes not written unless --write-hashes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
