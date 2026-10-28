"""S1/S2 ingest CLI."""

from __future__ import annotations

import argparse
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

from mirage_ablation.config.paths import (
    manifests_dir,
    raw_nsd_dir,
    raw_nsd_imagery_dir,
    runs_dir,
)
from mirage_ablation.config.schema import NsdImageryTestManifest
from mirage_ablation.config.subjects import SESSIONS
from mirage_ablation.ingest.probe import (
    run_format_probe,
    validate_probe_report,
    write_probe_json,
)
from mirage_ablation.ingest.s1_run import run_s1_subject
from mirage_ablation.provenance import (
    ManifestHashError,
    make_run_id,
    new_run_record,
    verify_manifest_hashes,
    write_run_record,
)


def _parse_sessions(spec: str) -> tuple[int, int]:
    m = re.fullmatch(r"(\d+)-(\d+)", spec.strip())
    if not m:
        raise argparse.ArgumentTypeError("expected --sessions A-B (e.g. 1-2)")
    lo, hi = int(m.group(1)), int(m.group(2))
    if lo < 1 or hi < lo:
        raise argparse.ArgumentTypeError("invalid session range")
    return lo, hi


def _load_manifest(path: Path) -> NsdImageryTestManifest:
    return NsdImageryTestManifest.model_validate_json(path.read_text())


def _run_probe(args: argparse.Namespace, manifest_hashes: dict[str, str]) -> int:
    if args.subject is None:
        print("--subject required for probe", file=sys.stderr)
        return 2
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


def _run_s1(args: argparse.Namespace, manifest_hashes: dict[str, str]) -> int:
    if args.manifest is None:
        print("--manifest required for S1", file=sys.stderr)
        return 2
    manifest_path = Path(args.manifest)
    if not manifest_path.is_file():
        manifest_path = manifests_dir() / args.manifest
    manifest = _load_manifest(manifest_path)

    subjects: list[int]
    if args.all_subjects:
        subjects = sorted(SESSIONS.keys())
    elif args.subject is not None:
        subjects = [args.subject]
    else:
        print("S1 requires --subject or --all-subjects", file=sys.stderr)
        return 2

    session_range = _parse_sessions(args.sessions) if args.sessions else None
    exit_code = 0

    for subject in subjects:
        run_id = make_run_id("S1", None, subject=subject)
        report_path = runs_dir() / run_id / "s1_report.json"
        started = datetime.now(timezone.utc)
        try:
            report = run_s1_subject(
                subject=subject,
                beta_version=args.beta_version,
                manifest=manifest,
                raw_nsd=raw_nsd_dir(),
                raw_imagery=raw_nsd_imagery_dir(),
                session_range=session_range,
                overwrite=args.overwrite,
                run_id=run_id,
                report_path=report_path,
            )
        except FileExistsError as exc:
            print(str(exc), file=sys.stderr)
            return 1
        except Exception as exc:
            print(f"S1 FAIL subj{subject:02d}: {exc}", file=sys.stderr)
            return 1

        record = new_run_record(
            run_id=run_id,
            stage_id="S1",
            subject_id=subject,
            beta_version=args.beta_version,
            manifest_hashes=manifest_hashes,
        )
        paths = resolve_output_paths(subject, session_range is not None)
        record.output_paths = [str(p) for p in paths]
        record.finished_at = datetime.now(timezone.utc).isoformat()
        record.exit_code = 0 if report.get("pass") else 1
        write_run_record(
            record,
            stage_meta={
                "argv": sys.argv,
                "report": str(report_path),
                "duration_seconds": (
                    datetime.now(timezone.utc) - started
                ).total_seconds(),
            },
        )
        if not report.get("pass"):
            print(f"S1 report FAIL → {report_path}", file=sys.stderr)
            exit_code = 1
        else:
            print(f"S1 PASS subj{subject:02d} → {report_path}")
    return exit_code


def resolve_output_paths(subject: int, smoke: bool) -> tuple[Path, ...]:
    from mirage_ablation.ingest.s1_run import resolve_s1_paths

    p = resolve_s1_paths(subject, smoke=smoke)
    return (
        p.perception_h5,
        p.imagery_h5,
        p.perception_parquet,
        p.imagery_parquet,
        p.mask_npz,
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Track B ingest stages")
    parser.add_argument("--stage", choices=["S1", "S2"], required=True)
    parser.add_argument("--manifest", type=str, default=None)
    parser.add_argument("--subject", type=int, default=None)
    parser.add_argument("--all-subjects", action="store_true")
    parser.add_argument(
        "--beta-version",
        choices=["betas_fithrf_GLMdenoise_RR", "betas_fithrf"],
        required=True,
    )
    parser.add_argument(
        "--sessions",
        type=str,
        default=None,
        help="Smoke only: inclusive session range A-B (writes under _smoke/)",
    )
    parser.add_argument("--probe", action="store_true")
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args(argv)

    if args.stage == "S2":
        print("S2 not implemented (IP-3)", file=sys.stderr)
        return 2

    try:
        manifest_hashes = verify_manifest_hashes()
    except ManifestHashError as exc:
        print(f"manifest hash gate: {exc}", file=sys.stderr)
        return 1

    if args.probe:
        return _run_probe(args, manifest_hashes)
    return _run_s1(args, manifest_hashes)


if __name__ == "__main__":
    raise SystemExit(main())
