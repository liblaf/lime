import functools
from collections.abc import Mapping
from typing import Self

import litellm
import pydantic

from liblaf.lime import utils


class CompletionRequest(utils.BaseModel):
    model: str = pydantic.Field(default="deepseek/deepseek-chat")
    temperature: float | None = pydantic.Field(default=None)


class ModelConfig(utils.BaseModel, litellm.ModelConfig):
    tpm: int | None = None  # pyright: ignore[reportIncompatibleVariableOverride]
    rpm: int | None = None  # pyright: ignore[reportIncompatibleVariableOverride]

    @classmethod
    def default_model_list(cls) -> list[Self]:
        return [
            cls(
                model_name="deepseek-chat",
                litellm_params=litellm.CompletionRequest(
                    model="deepseek/deepseek-chat"
                ),
            ),
            cls(
                model_name="deepseek-reasoner",
                litellm_params=litellm.CompletionRequest(
                    model="deepseek/deepseek-reasoner"
                ),
            ),
        ]


class RouterConfig(utils.BaseModel, litellm.RouterConfig):
    model_list: list[ModelConfig] = pydantic.Field(  # pyright: ignore[reportIncompatibleVariableOverride]
        default_factory=ModelConfig.default_model_list
    )

    @functools.cached_property
    def router(self) -> litellm.Router:
        return litellm.Router(**self.model_dump(exclude_unset=True, exclude_none=True))


class LiteLLMConfig(utils.BaseModel):
    completion: CompletionRequest = pydantic.Field(default_factory=CompletionRequest)
    router: RouterConfig = pydantic.Field(default_factory=RouterConfig)

    async def acompletion(
        self,
        model: str | None = None,
        messages: list[litellm.AllMessageValues] | None = None,
        prompt: str | None = None,
        **kwargs,
    ) -> litellm.CustomStreamWrapper:
        kwargs["model"] = model or self.completion.model
        if messages:
            kwargs["messages"] = messages
        elif prompt:
            kwargs["messages"] = [{"role": "user", "content": prompt}]
        kwargs["stream"] = True
        kwargs: Mapping = utils.merge(
            self.completion.model_dump(exclude_unset=True, exclude_none=True), kwargs
        )
        return await self.router.router.acompletion(**kwargs)


def litellm_config() -> LiteLLMConfig:
    return utils.load_config(LiteLLMConfig, "litellm")
