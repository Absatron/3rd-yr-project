"""Run IDs, manifest hash gate, and run records."""

from __future__ import annotations

import hashlib
import json
import os
import socket
import subprocess
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, Field

from mirage_ablation.config.paths import manifests_dir, repo_root, runs_dir


class ManifestHashError(RuntimeError):
    """Manifest bytes or registry hash mismatch."""


class RunRecord(BaseModel):
    """Fields required by the execution plan run.json schema plus ingest extensions."""

    run_id: str
    stage_id: str
    track: str = "B"
    setting: str | None = None
    condition: str | None = None
    subject_id: int | None = None
    manifest_version: str | None = None
    manifest_sha256: str | None = None
    audit_sha256: str | None = None
    git_commit: str | None = None
    mirage_fork_commit: str | None = None
    mirage_notebook_commit: str | None = None
    lambda_vdvae: float | None = None
    lambda_image_cls: float | None = None
    lambda_text: float | None = None
    lambda_retrieval: float | None = None
    seeds: list[int] = Field(default_factory=lambda: [42, 123, 456])
    reconstructions_per_seed: int = 10
    started_at: str
    finished_at: str | None = None
    exit_code: int | None = None
    artifact_paths: list[str] = Field(default_factory=list)
    host: str | None = None
    slurm_job_id: int | None = None
    slurm_array_task_id: int | None = None
    slurm_partition: str | None = None
    scratch_path: str | None = None
    beta_version: str | None = None
    input_hashes: dict[str, str] = Field(default_factory=dict)
    output_paths: list[str] = Field(default_factory=list)


def _today() -> str:
    return date.today().strftime("%Y%m%d")


def make_run_id(
    stage: str,
    setting: str | None,
    *,
    subject: int | None = None,
    extra: str | None = None,
) -> str:
    """Build a run ID per execution plan convention (C11)."""
    stage_lower = stage.lower()
    if setting is None:
        mid = f"{stage_lower}-shared"
    else:
        mid = f"{stage_lower}-setting_{setting.lower()}"
    parts = [_today(), mid]
    if extra:
        parts.append(extra)
    if subject is not None:
        parts.append(f"subj{subject:02d}")
    return "-".join(parts)


def _load_registry() -> dict[str, Any]:
    reg_path = repo_root() / "runs" / "registry.yaml"
    if not reg_path.is_file():
        return {}
    return yaml.safe_load(reg_path.read_text()) or {}


def _sidecar_hash(json_name: str) -> tuple[Path, str]:
    json_path = manifests_dir() / json_name
    sidecar = manifests_dir() / f"{json_name}.sha256"
    if not json_path.is_file():
        raise ManifestHashError(f"missing manifest file {json_path}")
    if not sidecar.is_file():
        raise ManifestHashError(
            f"missing hash sidecar for {json_name} (run s0_verify_manifests.py --write-hashes)"
        )
    expected = sidecar.read_text().split()[0]
    actual = hashlib.sha256(json_path.read_bytes()).hexdigest()
    if expected != actual:
        raise ManifestHashError(f"hash mismatch for {json_name}")
    return json_path, expected


def verify_manifest_hashes(
    *,
    check_registry: bool = True,
    manifest_names: tuple[str, ...] = (
        "nsd_imagery_test_manifest_v1.json",
        "stimulus_overlap_audit.json",
    ),
) -> dict[str, str]:
    """Verify manifest sidecars and optional registry provenance hashes."""
    hashes: dict[str, str] = {}
    for name in manifest_names:
        _, h = _sidecar_hash(name)
        hashes[name] = h

    if not check_registry:
        return hashes

    registry = _load_registry()
    provenance = registry.get("provenance") or {}
    reg_manifest = provenance.get("manifest_sha256")
    reg_audit = provenance.get("audit_sha256")

    manifest_h = hashes.get("nsd_imagery_test_manifest_v1.json")
    audit_h = hashes.get("stimulus_overlap_audit.json")

    if reg_manifest and manifest_h and reg_manifest != manifest_h:
        raise ManifestHashError(
            "registry provenance.manifest_sha256 does not match nsd_imagery_test_manifest sidecar"
        )
    if reg_audit and audit_h and reg_audit != audit_h:
        raise ManifestHashError(
            "registry provenance.audit_sha256 does not match stimulus_overlap_audit sidecar"
        )
    return hashes


def git_commit_short() -> str | None:
    try:
        out = subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            cwd=repo_root(),
            stderr=subprocess.DEVNULL,
            text=True,
        )
        return out.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def write_run_record(
    record: RunRecord,
    *,
    stage_meta: dict[str, Any] | None = None,
) -> Path:
    """Write run.json and stage_meta.yaml under runs_dir()/run_id/."""
    out_dir = runs_dir() / record.run_id
    out_dir.mkdir(parents=True, exist_ok=True)
    run_path = out_dir / "run.json"
    run_path.write_text(record.model_dump_json(indent=2))
    meta = stage_meta or {}
    meta.setdefault("run_id", record.run_id)
    meta.setdefault("exit_code", record.exit_code)
    (out_dir / "stage_meta.yaml").write_text(yaml.safe_dump(meta, sort_keys=False))
    return run_path


def slurm_env_fields() -> dict[str, Any]:
    """Capture Slurm environment when running under sbatch."""
    fields: dict[str, Any] = {}
    if job := os.environ.get("SLURM_JOB_ID"):
        try:
            fields["slurm_job_id"] = int(job)
        except ValueError:
            pass
    if task := os.environ.get("SLURM_ARRAY_TASK_ID"):
        try:
            fields["slurm_array_task_id"] = int(task)
        except ValueError:
            pass
    if part := os.environ.get("SLURM_JOB_PARTITION"):
        fields["slurm_partition"] = part
    return fields


def new_run_record(
    *,
    run_id: str,
    stage_id: str,
    setting: str | None = None,
    subject_id: int | None = None,
    beta_version: str | None = None,
    manifest_hashes: dict[str, str] | None = None,
) -> RunRecord:
    registry = _load_registry()
    study = registry.get("study") or {}
    provenance = registry.get("provenance") or {}
    mh = manifest_hashes or {}
    return RunRecord(
        run_id=run_id,
        stage_id=stage_id,
        setting=setting,
        subject_id=subject_id,
        manifest_version=study.get("manifest_version"),
        manifest_sha256=mh.get("nsd_imagery_test_manifest_v1.json")
        or provenance.get("manifest_sha256"),
        audit_sha256=mh.get("stimulus_overlap_audit.json")
        or provenance.get("audit_sha256"),
        git_commit=git_commit_short(),
        mirage_fork_commit=provenance.get("mirage_fork_commit"),
        mirage_notebook_commit=provenance.get("mirage_notebook_commit"),
        started_at=datetime.now(timezone.utc).isoformat(),
        host=socket.gethostname(),
        scratch_path=os.environ.get("MIRAGE_ABLATION_DATA_ROOT"),
        beta_version=beta_version,
        **slurm_env_fields(),
    )


def read_run_record(run_id: str) -> RunRecord:
    path = runs_dir() / run_id / "run.json"
    return RunRecord.model_validate_json(path.read_text())
