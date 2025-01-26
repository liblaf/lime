import json
import tempfile
from pathlib import Path
from typing import Any

from liblaf import lime


async def repomix(instruction: str | None = None) -> str:
    with tempfile.TemporaryDirectory() as tmpdir_:
        tmpdir = Path(tmpdir_)
        config_path: Path = tmpdir / "repomix.config.json"
        output_path: Path = tmpdir / "repomix-output.xml"
        # https://github.com/yamadashy/repomix#%EF%B8%8F-configuration
        config: dict[str, Any] = {
            "output": {"filePath": str(output_path), "style": "xml"},
            "ignore": {
                "customPatterns": [
                    "**/.*",
                    "**/*-lock.*",
                    "**/*.ipynb",
                    "**/*.lock",
                    "**/CHANGELOG.md",
                    "**/pyrightconfig.json",
                    "**/README.md",
                ]
            },
        }
        if instruction:
            instruction_path: Path = tmpdir / "repomix-instruction.md"
            instruction_path.write_text(instruction)
            config["output"]["instructionFilePath"] = str(instruction_path)
        # TODO: Add custom ignore patterns
        config_path.write_text(json.dumps(config))
        await lime.run(["repomix", "--config", config_path])
        return output_path.read_text()
