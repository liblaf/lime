import dataclasses
import importlib.resources
import os
import re
import string
from collections.abc import Mapping
from importlib.abc import Traversable
from pathlib import Path
from typing import Self

import frontmatter
import litellm


@dataclasses.dataclass(kw_only=True)
class Prompt:
    system: str | None = None
    prompt: str | None = None
    prefix: str | None = None

    @classmethod
    def from_markdown(cls, markdown: str) -> Self:
        post: frontmatter.Post = frontmatter.loads(markdown)
        content: str = post.content
        content = re.sub(r"<!--.*-->", "", content)
        content = re.sub(r"\n{2,}", "\n", content)
        return cls(
            system=post.get("system"),  # pyright: ignore[reportArgumentType]
            prompt=content,
            prefix=post.get("prefix"),  # pyright: ignore[reportArgumentType]
        )

    @property
    def messages(self) -> list[litellm.AllMessageValues]:
        messages: list[litellm.AllMessageValues] = []
        if self.system:
            messages.append({"role": "system", "content": self.system})
        if self.prompt:
            messages.append({"role": "user", "content": self.prompt})
        if self.prefix:
            messages.append(
                {"role": "assistant", "content": self.prefix, "prefix": True}  # pyright: ignore[reportArgumentType]
            )
        return messages

    def substitiute(
        self, mapping: Mapping[str, str] = {}, **kwargs: str
    ) -> list[litellm.AllMessageValues]:
        mapping = {**mapping, **kwargs}
        messages: list[litellm.AllMessageValues] = self.messages
        for message in messages:
            template = string.Template(message["content"])  # pyright: ignore[reportArgumentType, reportTypedDictNotRequiredAccess]
            message["content"] = template.substitute(mapping)
        return messages


def get_prompt(name: str | os.PathLike[str]) -> Prompt:
    markdown: str
    try:
        markdown = read_text_custom(name)
    except FileNotFoundError:
        markdown = read_text_preset(name)  # pyright: ignore[reportArgumentType]
    return Prompt.from_markdown(markdown)


def read_text_preset(name: str) -> str:
    prompts_dir: Traversable = importlib.resources.files("liblaf.lime.assets.prompts")
    path: Traversable = prompts_dir / f"{name}.md"
    return path.read_text()


def read_text_custom(path: str | os.PathLike[str]) -> str:
    path = Path(path)
    return path.read_text()
