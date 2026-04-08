from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from ..schemas.generation import GenerationRequest, GenerationResult
from .io import ensure_parent


def append_generation_log(
    log_path: str,
    request: GenerationRequest,
    result: GenerationResult,
) -> None:
    path = ensure_parent(log_path)
    record = {
        "request": asdict(request),
        "result": asdict(result),
    }
    with Path(path).open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
