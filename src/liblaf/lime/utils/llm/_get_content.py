from collections.abc import Callable, Sequence

import litellm

from liblaf import lime


def get_content(
    response: litellm.ModelResponse,
    *,
    messages: Sequence[litellm.AllMessageValues] = [],
    prefix: str | None = None,
    sanitizer: Callable[[str], str] | None = lime.extract_between_tags,
) -> str:
    content: str = litellm.get_content_from_model_response(response)
    if prefix is None:
        for message in messages:
            if (
                (message.get("role") == "assistant")
                and message.get("content")
                and message.get("prefix")
            ):
                prefix = message.get("content")  # pyright: ignore[reportAssignmentType]
                break
    if prefix and (not content.startswith(prefix)):
        content = prefix + content
    if sanitizer:
        content = sanitizer(content)
    return content
