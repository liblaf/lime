from collections.abc import Callable

import litellm
import rich
import rich.markup
from rich.console import Group, RenderableType
from rich.live import Live
from rich.markdown import Markdown
from rich.text import Text

from liblaf import lime


async def live(
    messages: list[litellm.AllMessageValues],
    *,
    markdown: bool = False,
    sanitizer: Callable[[str], str] | None = lime.extract_between_tags,
    temperature: float | None = None,
    title: RenderableType | None = None,
    transient: bool = False,
) -> str:
    cfg: lime.Config = lime.get_config()
    router: litellm.Router = cfg.router.build()
    stream: litellm.CustomStreamWrapper = await router.acompletion(
        messages=messages,
        temperature=temperature,
        stream=True,
        stream_options={"include_usage": True},
        **cfg.completion_kwargs,
    )
    chunks: list[litellm.ModelResponseStream] = []
    response = litellm.ModelResponse()
    with Live(transient=transient) as live:
        async for chunk in stream:
            chunks.append(chunk)
            response: litellm.ModelResponse = litellm.stream_chunk_builder(chunks)  # pyright: ignore[reportAssignmentType]
            content: str = lime.get_content(
                response, messages=messages, sanitizer=sanitizer
            )
            rich_content: RenderableType = _rich_content(
                content, markdown=markdown, response=response, title=title
            )
            live.update(rich_content)
    content: str = lime.get_content(response, messages=messages, sanitizer=sanitizer)
    return content


def _rich_content(
    content: str,
    *,
    markdown: bool = False,
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
    if markdown:
        renderables.append(Markdown(content))
    else:
        renderables.append(rich.markup.escape(content))
    return Group(*renderables)
