from collections.abc import Callable

import litellm
from rich.console import Group, RenderableType
from rich.live import Live
from rich.text import Text

from liblaf import lime


async def live(
    prompt: str,
    *,
    prefix: str | None = None,
    sanitizer: Callable[[str], str] | None = lime.extract_between_tags,
    title: RenderableType | None = None,
) -> str:
    cfg: lime.Config = lime.get_config()
    router: litellm.Router = cfg.router.build()
    messages: list[litellm.AllMessageValues] = [{"role": "user", "content": prompt}]
    if prefix:
        messages.append({"role": "assistant", "content": prefix, "prefix": True})  # pyright: ignore[reportArgumentType]
    stream: litellm.CustomStreamWrapper = await router.acompletion(
        messages=messages,
        stream=True,
        stream_options={"include_usage": True},
        **cfg.completion_kwargs,
    )
    chunks: list[litellm.ModelResponseStream] = []
    response = litellm.ModelResponse()
    with Live() as live:
        async for chunk in stream:
            chunks.append(chunk)
            response: litellm.ModelResponse = litellm.stream_chunk_builder(chunks)  # pyright: ignore[reportAssignmentType]
            content: str = lime.get_content(
                response, prefix=prefix, sanitizer=sanitizer
            )
            rich_content: RenderableType = _rich_content(
                content, response=response, title=title
            )
            live.update(rich_content)
    content: str = lime.get_content(response, prefix=prefix, sanitizer=sanitizer)
    return content


def _rich_content(
    content: str,
    *,
    response: litellm.ModelResponse | None = None,
    title: RenderableType | None = None,
) -> RenderableType:
    renderables: list[RenderableType] = []
    if (title is None) and response and response.model:
        title = "🤖 " + response.model
    if title:
        if isinstance(title, str):
            title = Text(title, style="bold cyan")
        renderables.append(title)
    renderables.append(content)
    return Group(*renderables)
