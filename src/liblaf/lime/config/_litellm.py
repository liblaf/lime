import litellm
import pydantic


class ModelConfig(litellm.ModelConfig):
    tpm: int | None = None  # pyright: ignore[reportIncompatibleVariableOverride]
    rpm: int | None = None  # pyright: ignore[reportIncompatibleVariableOverride]


def default_model_list() -> list[ModelConfig]:
    return [
        ModelConfig(
            model_name="deepseek-chat",
            litellm_params=litellm.CompletionRequest(model="deepseek/deepseek-chat"),
        )
    ]


class RouterConfig(litellm.RouterConfig):
    model_list: list[ModelConfig] = pydantic.Field(default_factory=default_model_list)  # pyright: ignore[reportIncompatibleVariableOverride]

    def build(self) -> litellm.Router:
        return litellm.Router(**self.model_dump())
