from __future__ import annotations

import importlib
import importlib.util
from pathlib import Path
from typing import Any

from .t2i_base import T2IBackend
from ..schemas.generation import GenerationRequest, ImageArtifact


class SDXLBackend(T2IBackend):
    """SDXL backend.

    If `diffusers` + `torch` are available, this backend uses a real SDXL
    pipeline. Otherwise it falls back to deterministic placeholder generation
    so the rest of the system remains runnable.
    """

    def __init__(
        self,
        model_id: str = "stabilityai/stable-diffusion-xl-base-1.0",
        device: str | None = None,
        torch_dtype: str = "float16",
        local_files_only: bool = False,
        variant: str = "fp16",
        use_safetensors: bool = True,
    ) -> None:
        self.model_id = model_id
        self.device = device
        self.torch_dtype = torch_dtype
        self.local_files_only = local_files_only
        self.variant = variant
        self.use_safetensors = use_safetensors
        self._pipe: Any | None = None
        self._init_error: Exception | None = None

        self._try_init_pipeline()

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

        if self._pipe is not None:
            images = self._generate_with_pipeline(request)
            for i, image in enumerate(images):
                path = output_dir / f"{request_id}_{i:02d}.png"
                image.save(path)
                artifacts.append(ImageArtifact(path=str(path), index=i))
            return artifacts

        if importlib.util.find_spec("PIL") is None:
            for i in range(request.num_images):
                path = output_dir / f"{request_id}_{i:02d}.txt"
                path.write_text(
                    f"backend=sdxl\nprompt={request.prompt}\nseed={request.seed}\n",
                    encoding="utf-8",
                )
                artifacts.append(ImageArtifact(path=str(path), index=i))
            return artifacts
        Image = importlib.import_module("PIL.Image")
        ImageDraw = importlib.import_module("PIL.ImageDraw")
        for i in range(request.num_images):
            path = output_dir / f"{request_id}_{i:02d}.png"
            img = Image.new("RGB", (request.width, request.height), color=(250, 250, 250))
            draw = ImageDraw.Draw(img)
            draw.text((12, 12), f"SDXL STUB\n{request.prompt[:100]}", fill=(0, 0, 0))
            img.save(path)
            artifacts.append(ImageArtifact(path=str(path), index=i))

        return artifacts

    def _try_init_pipeline(self) -> None:
        if importlib.util.find_spec("torch") is None or importlib.util.find_spec("diffusers") is None:
            self._init_error = RuntimeError("Missing torch/diffusers dependencies.")
            return
        try:
            torch = importlib.import_module("torch")
            diffusers = importlib.import_module("diffusers")
            StableDiffusionXLPipeline = getattr(diffusers, "StableDiffusionXLPipeline")

            if self.device is None:
                self.device = "cuda" if torch.cuda.is_available() else "cpu"

            dtype_map = {
                "float16": torch.float16,
                "float32": torch.float32,
                "bfloat16": torch.bfloat16,
            }
            selected_dtype = dtype_map.get(self.torch_dtype, torch.float16)
            if self.device == "cpu":
                selected_dtype = torch.float32

            self._pipe = StableDiffusionXLPipeline.from_pretrained(
                self.model_id,
                torch_dtype=selected_dtype,
                local_files_only=self.local_files_only,
                variant=self.variant,
                use_safetensors=self.use_safetensors,
            )
            self._pipe = self._pipe.to(self.device)
        except Exception as exc:
            self._pipe = None
            self._init_error = exc

    def _generate_with_pipeline(self, request: GenerationRequest) -> list[Any]:
        import torch

        generator = None
        if request.seed is not None:
            generator = torch.Generator(device=self.device).manual_seed(request.seed)

        output = self._pipe(
            prompt=request.prompt,
            negative_prompt=request.negative_prompt,
            width=request.width,
            height=request.height,
            num_inference_steps=request.steps,
            guidance_scale=request.guidance_scale,
            num_images_per_prompt=request.num_images,
            generator=generator,
        )
        return list(output.images)
