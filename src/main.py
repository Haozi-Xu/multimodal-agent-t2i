from __future__ import annotations

import argparse
import json

from .models.generator_service import GeneratorService
from .schemas.generation import GenerationRequest

DEFAULT_CONFIG = {
    "generator": {
        "backend": "sdxl",
        "output_dir": "outputs/generations",
        "log_file": "outputs/logs/generation.jsonl",
        "width": 512,
        "height": 512,
        "steps": 30,
        "guidance_scale": 7.5,
    }
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run generator service")
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--negative-prompt", default=None)
    parser.add_argument("--config", default="configs/base.yaml")
    parser.add_argument("--backend", default=None)
    parser.add_argument("--num-images", type=int, default=1)
    parser.add_argument("--seed", type=int, default=None)
    return parser.parse_args()


def load_config(path: str) -> dict:
    try:
        import yaml  # type: ignore
    except ImportError:
        return DEFAULT_CONFIG

    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def main() -> None:
    args = parse_args()
    conf = load_config(args.config)["generator"]

    backend = args.backend or conf["backend"]
    request = GenerationRequest(
        prompt=args.prompt,
        negative_prompt=args.negative_prompt,
        width=conf["width"],
        height=conf["height"],
        steps=conf["steps"],
        guidance_scale=conf["guidance_scale"],
        seed=args.seed,
        num_images=args.num_images,
        metadata={"config": args.config},
    )

    service = GeneratorService(
        backend=backend,
        output_dir=conf["output_dir"],
        log_file=conf["log_file"],
    )
    result = service.run(request)
    print(
        json.dumps(
            {
                "request_id": result.request_id,
                "backend": result.backend,
                "images": [x.path for x in result.images],
                "latency_ms": result.latency_ms,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
