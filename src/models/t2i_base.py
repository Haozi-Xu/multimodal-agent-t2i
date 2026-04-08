from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path

from ..schemas.generation import GenerationRequest, ImageArtifact


class T2IBackend(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def generate(
        self,
        request: GenerationRequest,
        output_dir: Path,
        request_id: str,
    ) -> list[ImageArtifact]:
        pass
