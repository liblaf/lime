import functools
from collections.abc import Callable
from typing import overload

import litellm


@overload
def extract_between_tags(
    *, tag: str = "answer"
) -> Callable[[str | litellm.ModelResponse], str]: ...
@overload
def extract_between_tags(
    content: str | litellm.ModelResponse, /, tag: str = "answer"
) -> str: ...
def extract_between_tags(
    content: str | litellm.ModelResponse | None = None, /, tag: str = "answer"
) -> str | Callable:
    if content is None:
        return functools.partial(extract_between_tags, tag=tag)
    if isinstance(content, litellm.ModelResponse):
        content = litellm.get_content_from_model_response(content)
    tag = tag.lower()
    tag_start: str = f"<{tag}>"
    start: int = content.lower().find(tag_start)
    if start >= 0:
        start += len(tag_start)
        content = content[start:]
    tag_end: str = f"</{tag}>"
    end: int = content.lower().find(tag_end)
    if end >= 0:
        content = content[:end]
    return content.strip()
