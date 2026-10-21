#!/usr/bin/env python3
"""Selective MIRAGE HF download (no full ~300GB bundle)."""

from __future__ import annotations

import argparse
import os
from pathlib import Path

from huggingface_hub import snapshot_download


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dest",
        type=Path,
        default=Path(
            os.environ.get(
                "MIRAGE_ABLATION_DATA_ROOT",
                Path.home() / "scratch/comp30030-mirage-ablation/data",
            )
        )
        / "frozen_weights"
        / "mirage_hf",
    )
    parser.add_argument(
        "--repo",
        default="reesekneeland/MIRAGE",
        help="HF dataset repo id",
    )
    args = parser.parse_args()

    args.dest.mkdir(parents=True, exist_ok=True)
    # M0/M1 selective patterns — expand after inspecting HF tree; captions + CLIP first.
    allow_patterns = [
        "*caption*",
        "*clip*",
        "*.json",
        ".gitattributes",
    ]
    path = snapshot_download(
        repo_id=args.repo,
        repo_type="dataset",
        allow_patterns=allow_patterns,
        local_dir=str(args.dest),
        local_dir_use_symlinks=False,
    )
    print(f"downloaded selective artifacts to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
