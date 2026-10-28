"""Unit tests for path helpers."""

from __future__ import annotations

from mirage_ablation.config.paths import (
    betas_dir,
    betas_masked_dir,
    manifest_sha_short,
    processed_dir,
    smoke_root,
    splits_dir,
    targets_dir,
)


def test_processed_layout(repo_layout):
    assert processed_dir().name == "processed"
    assert betas_dir(1) == processed_dir() / "betas" / "subj01"
    assert betas_masked_dir(8) == processed_dir() / "betas_masked" / "subj08"
    assert targets_dir() == processed_dir() / "targets"
    assert smoke_root() == processed_dir() / "_smoke"
    sha = "abcd" * 16
    assert manifest_sha_short(sha) == sha[:12]
    assert splits_dir("deadbeefcafe", "A") == (
        processed_dir() / "splits" / "deadbeefcafe" / "setting_a"
    )
