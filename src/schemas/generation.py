from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class GenerationRequest:
    prompt: str
    negative_prompt: str | None = None
    width: int = 512
    height: int = 512
    steps: int = 30
    guidance_scale: float = 7.5
    seed: int | None = None
    num_images: int = 1
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class ImageArtifact:
    path: str
    index: int


@dataclass
class GenerationResult:
    request_id: str
    backend: str
    images: list[ImageArtifact]
    latency_ms: int
    started_at: str
    ended_at: str
    request: GenerationRequest
    metadata: dict[str, Any] = field(default_factory=dict)
