from __future__ import annotations

from pathlib import Path

from .t2i_base import T2IBackend
from ..schemas.generation import GenerationRequest, ImageArtifact


class SDXLBackend(T2IBackend):
    """SDXL backend stub.

    Current behavior is deterministic placeholder generation to keep the
    pipeline runnable before plugging real model weights/providers.
    """

    @property
    def name(self) -> str:
        return "sdxl"

    def generate(
        self,
        request: GenerationRequest,
        output_dir: Path,
        request_id: str,
    ) -> list[ImageArtifact]:
        output_dir.mkdir(parents=True, exist_ok=True)
        artifacts: list[ImageArtifact] = []

        try:
            from PIL import Image, ImageDraw
        except ImportError:
            for i in range(request.num_images):
                path = output_dir / f"{request_id}_{i:02d}.txt"
                path.write_text(
                    f"backend=sdxl\nprompt={request.prompt}\nseed={request.seed}\n",
                    encoding="utf-8",
                )
                artifacts.append(ImageArtifact(path=str(path), index=i))
            return artifacts

        for i in range(request.num_images):
            path = output_dir / f"{request_id}_{i:02d}.png"
            img = Image.new("RGB", (request.width, request.height), color=(250, 250, 250))
            draw = ImageDraw.Draw(img)
            draw.text((12, 12), f"SDXL STUB\n{request.prompt[:100]}", fill=(0, 0, 0))
            img.save(path)
            artifacts.append(ImageArtifact(path=str(path), index=i))

        return artifacts
