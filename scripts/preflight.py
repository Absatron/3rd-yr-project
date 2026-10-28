#!/usr/bin/env python3
"""Preflight checks before training (manifest hashes, data layout)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from mirage_ablation.config.paths import manifests_dir, raw_nsd_dir, raw_nsd_imagery_dir
from mirage_ablation.provenance import ManifestHashError, verify_manifest_hashes


def _check_sidecar(json_name: str) -> list[str]:
    try:
        verify_manifest_hashes(
            check_registry=False,
            manifest_names=(json_name,),
        )
    except ManifestHashError as exc:
        return [str(exc)]
    return []


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
