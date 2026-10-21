#!/usr/bin/env python3
"""Preflight checks before training (manifest hashes, data layout)."""

from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from mirage_ablation.config.paths import manifests_dir, raw_nsd_dir, raw_nsd_imagery_dir


def _check_sidecar(json_name: str) -> list[str]:
    issues: list[str] = []
    json_path = manifests_dir() / json_name
    sidecar = manifests_dir() / f"{json_name}.sha256"
    if not json_path.is_file():
        issues.append(f"missing {json_path}")
        return issues
    if not sidecar.is_file():
        issues.append(f"missing hash sidecar for {json_name} (run s0_verify_manifests.py --write-hashes)")
        return issues
    expected = sidecar.read_text().split()[0]
    actual = hashlib.sha256(json_path.read_bytes()).hexdigest()
    if expected != actual:
        issues.append(f"hash mismatch for {json_name}")
    return issues


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--leakage-checklist",
        action="store_true",
        help="Run HG-1 leakage checklist (requires S4; stub until then).",
    )
    args = parser.parse_args()

    issues: list[str] = []
    issues.extend(_check_sidecar("nsd_imagery_test_manifest_v1.json"))
    issues.extend(_check_sidecar("stimulus_overlap_audit.json"))

    cue = raw_nsd_imagery_dir() / "experiments" / "nsdimagery" / "cue_pair_list.xlsx"
    if not cue.is_file():
        issues.append(f"missing imagery metadata: {cue}")

    stim = raw_nsd_dir() / "experiments" / "nsd" / "nsd_stim_info_merged.csv"
    if not stim.is_file():
        issues.append(f"missing NSD stim info: {stim}")

    if args.leakage_checklist:
        print("leakage checklist: not implemented until S4 (HG-1)")

    if issues:
        for i in issues:
            print(f"FAIL: {i}", file=sys.stderr)
        return 1

    print("preflight: PASS (manifest files present; HG-0 sign-off still required before training)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
