"""Unit tests for run IDs and manifest hash gate."""

from __future__ import annotations

import hashlib
from datetime import date

import pytest
import yaml

from mirage_ablation.provenance import (
    ManifestHashError,
    RunRecord,
    make_run_id,
    verify_manifest_hashes,
    write_run_record,
)


def test_make_run_id_patterns():
    today = date.today().strftime("%Y%m%d")
    assert make_run_id("S2", "A", subject=1) == f"{today}-s2-setting_a-subj01"
    assert make_run_id("S1", None, subject=1) == f"{today}-s1-shared-subj01"


def test_verify_manifest_hashes_match(repo_layout):
    root = repo_layout
    manifest = root / "manifests" / "nsd_imagery_test_manifest_v1.json"
    manifest.write_text("{}")
    digest = hashlib.sha256(manifest.read_bytes()).hexdigest()
    (root / "manifests" / "nsd_imagery_test_manifest_v1.json.sha256").write_text(
        f"{digest}  nsd_imagery_test_manifest_v1.json\n"
    )
    reg = {
        "provenance": {
            "manifest_sha256": digest,
        }
    }
    (root / "runs" / "registry.yaml").write_text(yaml.dump(reg))
    out = verify_manifest_hashes(
        manifest_names=("nsd_imagery_test_manifest_v1.json",),
    )
    assert out["nsd_imagery_test_manifest_v1.json"] == digest


def test_verify_manifest_registry_mismatch(repo_layout):
    root = repo_layout
    manifest = root / "manifests" / "stimulus_overlap_audit.json"
    manifest.write_text("{}")
    digest = hashlib.sha256(manifest.read_bytes()).hexdigest()
    (root / "manifests" / "stimulus_overlap_audit.json.sha256").write_text(
        f"{digest}  stimulus_overlap_audit.json\n"
    )
    (root / "runs" / "registry.yaml").write_text(
        yaml.dump({"provenance": {"audit_sha256": "0" * 64}})
    )
    with pytest.raises(ManifestHashError):
        verify_manifest_hashes(manifest_names=("stimulus_overlap_audit.json",))


def test_run_record_roundtrip(repo_layout, monkeypatch):
    monkeypatch.setenv("MIRAGE_ABLATION_RUNS_ROOT", str(repo_layout / "runs"))
    rec = RunRecord(
        run_id="test-run",
        stage_id="S1",
        started_at="2026-10-28T00:00:00+00:00",
        manifest_sha256="a" * 64,
        audit_sha256="b" * 64,
        git_commit="deadbeef",
        artifact_paths=[],
    )
    path = write_run_record(rec, stage_meta={"argv": ["probe"]})
    assert path.is_file()
    assert (path.parent / "stage_meta.yaml").is_file()
