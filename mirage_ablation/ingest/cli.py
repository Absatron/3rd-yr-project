"""S1/S2 ingest CLI (probe mode in IP-1)."""

from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone

from mirage_ablation.config.paths import runs_dir
from mirage_ablation.ingest.probe import (
    run_format_probe,
    validate_probe_report,
    write_probe_json,
)
from mirage_ablation.provenance import (
    ManifestHashError,
    new_run_record,
    verify_manifest_hashes,
    write_run_record,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Track B ingest stages")
    parser.add_argument("--stage", choices=["S1", "S2"], required=True)
    parser.add_argument("--manifest", type=str, default=None)
    parser.add_argument("--subject", type=int, default=None)
    parser.add_argument(
        "--beta-version",
        choices=["betas_fithrf_GLMdenoise_RR", "betas_fithrf"],
        required=True,
    )
    parser.add_argument("--probe", action="store_true")
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args(argv)

    if args.stage != "S1" or not args.probe:
        print("Only --stage S1 --probe is implemented in IP-1", file=sys.stderr)
        return 2

    if args.manifest is None:
        print("--manifest required for S1 probe", file=sys.stderr)
        return 2
    if args.subject is None:
        print("--subject required for probe", file=sys.stderr)
        return 2

    try:
        manifest_hashes = verify_manifest_hashes()
    except ManifestHashError as exc:
        print(f"manifest hash gate: {exc}", file=sys.stderr)
        return 1

    from mirage_ablation.provenance import make_run_id

    run_id = make_run_id("S1", None, subject=args.subject)
    out_dir = runs_dir() / run_id
    probe_path = out_dir / "format_probe.json"
    if probe_path.is_file() and not args.overwrite:
        print(f"refusing to overwrite {probe_path} (use --overwrite)", file=sys.stderr)
        return 1

    started = datetime.now(timezone.utc)
    report = run_format_probe(args.subject, args.beta_version)
    failures = validate_probe_report(report)
    report["validation_failures"] = failures
    report["validation_pass"] = len(failures) == 0

    write_probe_json(report, probe_path)

    record = new_run_record(
        run_id=run_id,
        stage_id="S1",
        subject_id=args.subject,
        beta_version=args.beta_version,
        manifest_hashes=manifest_hashes,
    )
    record.output_paths = [str(probe_path)]
    record.finished_at = datetime.now(timezone.utc).isoformat()
    record.exit_code = 0 if report["validation_pass"] else 1
    write_run_record(
        record,
        stage_meta={
            "argv": sys.argv,
            "inputs": {"manifest": args.manifest, "beta_version": args.beta_version},
            "outputs": [str(probe_path)],
            "duration_seconds": (datetime.now(timezone.utc) - started).total_seconds(),
        },
    )

    if failures:
        for f in failures:
            print(f"PROBE FAIL: {f}", file=sys.stderr)
        return 1

    print(f"probe PASS → {probe_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
