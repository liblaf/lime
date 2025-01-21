import importlib
import importlib.resources
import os
from importlib.abc import Traversable
from pathlib import Path


def prompt(name: str | os.PathLike[str]) -> str:
    try:
        return prompt_custom(name)
    except FileNotFoundError:
        return prompt_preset(name)  # pyright: ignore[reportArgumentType]


def prompt_preset(name: str) -> str:
    prompts_dir: Traversable = importlib.resources.files("liblaf.lime.assets.prompts")
    path: Traversable = prompts_dir / f"{name}.md"
    return path.read_text()


def prompt_custom(path: str | os.PathLike[str]) -> str:
    path = Path(path)
    return path.read_text()
