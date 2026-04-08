from __future__ import annotations

from pathlib import Path

from .t2i_base import T2IBackend
from ..schemas.generation import GenerationRequest, ImageArtifact


class FluxBackend(T2IBackend):
    """FLUX backend stub for architecture compatibility."""

    @property
    def name(self) -> str:
        return "flux"

    def generate(
        self,
        request: GenerationRequest,
        output_dir: Path,
        request_id: str,
    ) -> list[ImageArtifact]:
        output_dir.mkdir(parents=True, exist_ok=True)
        artifacts: list[ImageArtifact] = []

        for i in range(request.num_images):
            path = output_dir / f"{request_id}_{i:02d}.txt"
            path.write_text(
                f"backend=flux\nprompt={request.prompt}\nseed={request.seed}\n",
                encoding="utf-8",
            )
            artifacts.append(ImageArtifact(path=str(path), index=i))

        return artifacts
