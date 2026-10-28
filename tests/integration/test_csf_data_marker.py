"""Placeholder so ``pytest -m csf_data`` collects and skips on laptop."""

from __future__ import annotations

import os

import pytest


@pytest.mark.csf_data
def test_scratch_data_root_required():
    if not os.environ.get("MIRAGE_ABLATION_DATA_ROOT"):
        pytest.skip("MIRAGE_ABLATION_DATA_ROOT not set")
    pytest.fail("integration tests not implemented until IP-2")
