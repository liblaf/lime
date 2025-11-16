from collections.abc import Callable, Sequence
from typing import Any, Self, cast

import attrs
import litellm
from rich.console import Group
from rich.live import Live
from rich.spinner import Spinner
from rich.text import Text

from liblaf.lime import tools

from ._config import LLMConfig
from ._parse import LLMArgs


@attrs.define
class LLM:
    model: str | None = None
    router: litellm.Router = attrs.field(factory=litellm.Router)
    temperature: float | None = None
    base_url: str | None = None
    api_key: str | None = None

    @classmethod
    def from_args(cls, args: LLMArgs) -> Self:
        config = LLMConfig()
        model: str = (
            args.model or config.model or config.router.model_list[0].model_name
        )
        return cls(
            model=model,
            router=config.router.build(),
            temperature=args.temperature,
            base_url=args.base_url,
            api_key=args.api_key,
        )

    async def acompletion(
        self,
        messages: str | Sequence[litellm.AllMessageValues],
        model: str | None = None,
        **kwargs,
    ) -> litellm.CustomStreamWrapper:
        kwargs: dict[str, Any] = self._prepare_kwargs(
            messages=messages, model=model, **kwargs
        )
        return await self.router.acompletion(**kwargs)

    async def live(
        self,
        messages: str | Sequence[litellm.AllMessageValues],
        model: str | None = None,
        parser: Callable | None = None,
        **kwargs,
    ) -> litellm.ModelResponse:
        kwargs: dict[str, Any] = self._prepare_kwargs(
            messages=messages, model=model, **kwargs
        )
        model: str = kwargs["model"]
        stream: litellm.CustomStreamWrapper = await self.router.acompletion(**kwargs)
        chunks: list[litellm.ModelResponseStream | None] = []
        with Live(screen=True) as live:
            spinner: Spinner = Spinner(
                name="dots",
                text=Text(f"🤖 {model} (Waiting for response ...)", style="bold cyan"),
                style="bold cyan",
            )
            live.update(Group(spinner))
            async for chunk in stream:
                chunks.append(chunk)
                response: litellm.ModelResponse = litellm.stream_chunk_builder(chunks)  # pyright: ignore[reportAssignmentType]
                message: litellm.Message = response.choices[0].message  # pyright: ignore[reportAttributeAccessIssue]
                if response.model:
                    model = response.model
                if content := cast("str", message.content):
                    spinner.update(text=Text(f"🤖 {model}", style="bold cyan"))
                    if parser is not None:
                        content: str = parser(content)
                    live.update(Group(spinner, tools.Tail(Text(content), margin=1)))
                elif message.reasoning_content:
                    spinner.update(
                        text=Text(f"🤖 {model} (Reasoning ...)", style="bold cyan")
                    )
                    live.update(
                        Group(
                            spinner,
                            tools.Tail(
                                Text(message.reasoning_content, style="dim"), margin=1
                            ),
                        )
                    )
        response: litellm.ModelResponse = litellm.stream_chunk_builder(chunks)  # pyright: ignore[reportAssignmentType]
        return response

    def _prepare_kwargs(self, **kwargs) -> dict[str, Any]:
        if not kwargs.get("model"):
            kwargs["model"] = self.model
        messages: str | Sequence[litellm.AllMessageValues] = kwargs["messages"]
        if isinstance(messages, str):
            messages = [{"role": "user", "content": messages}]
        kwargs["messages"] = messages

        kwargs.setdefault("stream", True)
        kwargs.setdefault("stream_options", {"include_usage": True})
        if self.temperature is not None:
            kwargs.setdefault("temperature", self.temperature)
        if self.base_url is not None:
            kwargs.setdefault("base_url", self.base_url)
        if self.api_key is not None:
            kwargs.setdefault("api_key", self.api_key)

        return kwargs
