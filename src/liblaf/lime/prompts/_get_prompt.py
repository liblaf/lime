import importlib.resources
from importlib.resources.abc import Traversable

import jinja2


def get_prompt(prompt: str) -> jinja2.Template:
    folder: Traversable = importlib.resources.files(__name__)
    file: Traversable = folder / f"{prompt}.md"
    text: str = file.read_text()
    return jinja2.Template(text)
