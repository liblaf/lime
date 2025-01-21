import string
from collections.abc import Mapping, Sequence

import litellm


def prompt_template_substitute(
    template: Sequence[litellm.AllMessageValues],
    mapping: Mapping[str, str] = {},
    **kwargs: str,
) -> list[litellm.AllMessageValues]:
    messages: list[litellm.AllMessageValues] = []
    for message in template:
        if "content" in message and isinstance(message["content"], str):
            t = string.Template(message["content"])
            message["content"] = t.substitute({**mapping, **kwargs})
        messages.append(message)
    return messages
