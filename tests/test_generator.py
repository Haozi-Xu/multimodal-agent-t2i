from pathlib import Path

from src.models.generator_service import GeneratorService
from src.schemas.generation import GenerationRequest


def test_generator_service_generates_and_logs(tmp_path: Path) -> None:
    output_dir = tmp_path / "generations"
    log_file = tmp_path / "logs" / "generation.jsonl"

    service = GeneratorService(
        backend="sdxl",
        output_dir=str(output_dir),
        log_file=str(log_file),
    )
    result = service.run(GenerationRequest(prompt="a red fox", num_images=2, seed=1))

    assert result.backend == "sdxl"
    assert len(result.images) == 2
    for image in result.images:
        assert Path(image.path).exists()

    assert log_file.exists()
    lines = log_file.read_text(encoding="utf-8").strip().splitlines()
    assert len(lines) == 1
    assert "a red fox" in lines[0]
