"""Subject session counts and role sets (MIRAGE-aligned)."""

from __future__ import annotations

from mirage_ablation.s0.training_mask import TEST_SUBJECTS

TUNE_SUBJECTS: tuple[int, ...] = (3, 4, 6, 8)

SESSIONS: dict[int, int] = {
    1: 40,
    2: 40,
    3: 32,
    4: 30,
    5: 40,
    6: 32,
    7: 40,
    8: 30,
}

TRIALS_PER_SESSION: int = 750

__all__ = [
    "TEST_SUBJECTS",
    "TUNE_SUBJECTS",
    "SESSIONS",
    "TRIALS_PER_SESSION",
]
