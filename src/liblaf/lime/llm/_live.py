from collections.abc import Callable, Generator

import litellm
import rich
from rich.console import RenderableType
from rich.live import Live
from rich.text import Text


async def live(
    stream: litellm.CustomStreamWrapper,
    *,
    processor: Callable[[litellm.ModelResponse], litellm.ModelResponse] | None = None,
) -> litellm.ModelResponse:
    chunks: list[litellm.ModelResponseStream] = []
    with Live(transient=True, vertical_overflow="visible") as live:
        async for chunk in stream:
            chunks.append(chunk)
            response: litellm.ModelResponse = litellm.stream_chunk_builder(chunks)  # pyright: ignore[reportAssignmentType]
            if callable(processor):
                response = processor(response)
            live.update(_rich_content(response))
    response: litellm.ModelResponse = litellm.stream_chunk_builder(chunks)  # pyright: ignore[reportAssignmentType]
    if callable(processor):
        response = processor(response)
    return response


@rich.console.group()
def _rich_content(response: litellm.ModelResponse) -> Generator[RenderableType]:
    if response.model:
        yield Text(f"🤖 {response.model}", style="bold cyan")
    message: litellm.Message = response.choices[0].message  # pyright: ignore[reportAttributeAccessIssue]
    if message.content:
        yield Text(message.content)
    elif reasoning_content := getattr(message, "reasoning_content", None):
        yield Text(reasoning_content, style="dim")
