from collections.abc import Callable

import litellm

from liblaf import lime


def get_content(
    response: litellm.ModelResponse,
    *,
    prefix: str | None = None,
    sanitizer: Callable[[str], str] | None = lime.extract_between_tags,
) -> str:
    content: str = litellm.get_content_from_model_response(response)
    if prefix and (not content.startswith(prefix)):
        content = prefix + content
    if sanitizer:
        content = sanitizer(content)
    return content
