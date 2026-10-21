"""S0.4 — SHA-256 manifest for on-disk frozen weights."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from mirage_ablation.config.paths import frozen_weights_dir


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def build_weights_manifest(root: Path | None = None) -> dict:
    root = root or frozen_weights_dir()
    entries: list[dict] = []
    if root.is_dir():
        for path in sorted(root.rglob("*")):
            if path.is_file() and path.stat().st_size > 0:
                rel = path.relative_to(root)
                entries.append(
                    {
                        "relative_path": str(rel),
                        "sha256": _sha256_file(path),
                        "bytes": path.stat().st_size,
                    }
                )
    return {
        "hash_algorithm": "sha256",
        "root": str(root),
        "status": "empty" if not entries else "populated",
        "artifacts": entries,
    }


def write_weights_manifest(path: Path) -> dict:
    payload = build_weights_manifest()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n")
    return payload
