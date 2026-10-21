"""Unit tests for S0 manifest schema."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from mirage_ablation.config.schema import NsdImageryTestManifest
from mirage_ablation.s0.catalogue import build_test_manifest


@pytest.fixture
def synced_metadata(tmp_path, monkeypatch):
    """Minimal on-disk layout mimicking M0 AWS sync."""
    imagery = tmp_path / "data" / "raw" / "nsd_imagery" / "experiments" / "nsdimagery"
    nsd = tmp_path / "data" / "raw" / "nsd" / "experiments" / "nsd"
    imagery.mkdir(parents=True)
    nsd.mkdir(parents=True)

    # Copy real cue xlsx from /tmp if available, else build minimal zip xlsx
    src = Path("/tmp/nsd-meta/cue_pair_list.xlsx")
    if src.is_file():
        (imagery / "cue_pair_list.xlsx").write_bytes(src.read_bytes())
    else:
        pytest.skip("cue_pair_list.xlsx not available locally")

    stim_src = Path("/tmp/nsd-meta/nsd_stim_info_merged.csv")
    if stim_src.is_file():
        (nsd / "nsd_stim_info_merged.csv").write_bytes(stim_src.read_bytes())
    else:
        pytest.skip("nsd_stim_info_merged.csv not available locally")

    monkeypatch.setenv("MIRAGE_ABLATION_REPO", str(tmp_path))
    monkeypatch.setenv("MIRAGE_ABLATION_DATA_ROOT", str(tmp_path / "data"))
    return tmp_path


def test_build_manifest_eighteen_stimuli(synced_metadata):
    manifest = build_test_manifest()
    assert len(manifest.imagery_stimuli) == 18
    NsdImageryTestManifest.model_validate_json(manifest.model_dump_json())
