"""Unit tests for format probe helpers (synthetic fixtures)."""

from __future__ import annotations

from mirage_ablation.ingest.probe import _infer_voxel_order, validate_probe_report


def test_axis_permutation_exact_match(synthetic_nii_betas, synthetic_session_h5):
    result = _infer_voxel_order(synthetic_nii_betas, synthetic_session_h5, n_trials=10)
    assert result["voxel_order"] is not None


def test_validate_probe_synthetic_passes(synthetic_nii_betas, synthetic_session_h5):
    axis = _infer_voxel_order(synthetic_nii_betas, synthetic_session_h5)
    report = {
        "axis_probe": axis,
        "nsdgeneral_unique_values": [-1.0, 0.0, 1.0],
        "imagery_beta_trials": 576,
        "design_matrix_trials": 576,
        "imagery_trial_count_match": True,
        "mat_files": [{"reader": "scipy", "path": "x.mat"}],
    }
    assert validate_probe_report(report) == []
