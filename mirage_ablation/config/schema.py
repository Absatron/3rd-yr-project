"""Pydantic schemas for frozen manifests (S0)."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Literal

from pydantic import BaseModel, Field, field_validator


StimulusType = Literal["simple", "complex", "conceptual"]
ConditionName = Literal["image_only", "text_only", "combined"]


class ImageryStimulus(BaseModel):
    stimulus_id: str
    type: StimulusType
    letter_cue: str = Field(min_length=1, max_length=1)
    coco_id: int | None = None
    nsd_id: int | None = None
    target_label: str
    overlap_label: str
    strict_holdout: bool = True


class RetrievalDistractors(BaseModel):
    N: int = 50
    pool: str = "nsd_shared1000"
    distractor_resamples: int = 100


class Embedding2AFC(BaseModel):
    distractors_per_target: int = 5
    within_type: bool = True


class MetricsConfig(BaseModel):
    top_k: list[int] = Field(default_factory=lambda: [1, 5, 10])
    primary_k: int = 1


class TrainExclusions(BaseModel):
    shared1000: bool = True
    setting_b_semantic_threshold: float = 0.85


class NsdImageryTestManifest(BaseModel):
    version: str = "1.0.0"
    created: str
    hash_algorithm: str = "sha256"
    source_files: list[str] = Field(default_factory=list)
    subjects: list[int] = Field(default_factory=lambda: [1, 2, 5, 7])
    tuning_subjects: list[int] = Field(default_factory=lambda: [3, 4, 6, 8])
    imagery_stimuli: list[ImageryStimulus]
    train_exclusions: TrainExclusions = Field(default_factory=TrainExclusions)
    conditions: list[ConditionName] = Field(
        default_factory=lambda: ["image_only", "text_only", "combined"]
    )
    seeds: list[int] = Field(default_factory=lambda: [42, 123, 456])
    reconstructions_per_seed: int = 10
    retrieval_distractors: RetrievalDistractors = Field(
        default_factory=RetrievalDistractors
    )
    embedding_2afc: Embedding2AFC = Field(default_factory=Embedding2AFC)
    metrics: MetricsConfig = Field(default_factory=MetricsConfig)

    @field_validator("imagery_stimuli")
    @classmethod
    def exactly_eighteen_stimuli(cls, v: list[ImageryStimulus]) -> list[ImageryStimulus]:
        if len(v) != 18:
            raise ValueError(f"expected 18 imagery_stimuli, got {len(v)}")
        counts = {t: 0 for t in ("simple", "complex", "conceptual")}
        for s in v:
            counts[s.type] += 1
        if counts != {"simple": 6, "complex": 6, "conceptual": 6}:
            raise ValueError(f"expected 6 per type, got {counts}")
        return v

    @classmethod
    def now_iso(cls) -> str:
        return datetime.now(timezone.utc).replace(microsecond=0).isoformat()
