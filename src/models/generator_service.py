from __future__ import annotations

import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

from .flux_backend import FluxBackend
from .sdxl_backend import SDXLBackend
from .t2i_base import T2IBackend
from ..schemas.generation import GenerationRequest, GenerationResult
from ..utils.logging import append_generation_log


class GeneratorService:
    def __init__(
        self,
        backend: str = "sdxl",
        output_dir: str = "outputs/generations",
        log_file: str = "outputs/logs/generation.jsonl",
    ) -> None:
        self.output_dir = Path(output_dir)
        self.log_file = log_file

        self.backends: dict[str, T2IBackend] = {
            "sdxl": SDXLBackend(),
            "flux": FluxBackend(),
        }
        if backend not in self.backends:
            raise ValueError(f"Unsupported backend: {backend}")
        self.backend = self.backends[backend]

    def run(self, request: GenerationRequest) -> GenerationResult:
        request_id = uuid.uuid4().hex[:12]
        started_at = datetime.now(timezone.utc).isoformat()
        t0 = time.time()

        target_dir = self.output_dir / request_id
        images = self.backend.generate(request, target_dir, request_id)

        t1 = time.time()
        ended_at = datetime.now(timezone.utc).isoformat()

        result = GenerationResult(
            request_id=request_id,
            backend=self.backend.name,
            images=images,
            latency_ms=int((t1 - t0) * 1000),
            started_at=started_at,
            ended_at=ended_at,
            request=request,
            metadata={
                "output_dir": str(target_dir),
            },
        )
        append_generation_log(self.log_file, request, result)
        return result
