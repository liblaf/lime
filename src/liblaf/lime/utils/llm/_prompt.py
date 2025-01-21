import importlib.resources
import os
import re
from importlib.abc import Traversable
from pathlib import Path

import frontmatter
import litellm


def prompt(
    name: str | os.PathLike[str], *, strip: bool = True
) -> list[litellm.AllMessageValues]:
    try:
        content: str = prompt_custom(name)
    except FileNotFoundError:
        content: str = prompt_preset(name)  # pyright: ignore[reportArgumentType]
    post: frontmatter.Post = frontmatter.loads(content)
    messages: list[litellm.AllMessageValues] = []
    if "system" in post:
        messages.append({"role": "system", "content": post["system"]})  # pyright: ignore[reportArgumentType]
    if strip:
        content = re.sub(r"\n<!--.*-->\n", "\n", content)
        content = re.sub(r"<!--.*-->", "", content)
        content = content.strip()
    messages.append({"role": "user", "content": content})
    if "prefix" in post:
        messages.append(
            {"role": "assistant", "content": post["prefix"], "prefix": True}  # pyright: ignore[reportArgumentType]
        )
    return messages


def prompt_preset(name: str) -> str:
    prompts_dir: Traversable = importlib.resources.files("liblaf.lime.assets.prompts")
    path: Traversable = prompts_dir / f"{name}.md"
    return path.read_text()


def prompt_custom(path: str | os.PathLike[str]) -> str:
    path = Path(path)
    return path.read_text()
