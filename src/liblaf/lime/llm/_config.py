# pyright: reportIncompatibleVariableOverride=none

from collections.abc import Sequence
from typing import Any, override

import litellm
import platformdirs
import pydantic
import pydantic_settings as ps


class ModelConfig(litellm.ModelConfig):
    tpm: int | None = None
    rpm: int | None = None


class RouterConfig(litellm.RouterConfig, pydantic.BaseModel):
    model_list: list[ModelConfig] = [
        ModelConfig(
            model_name="gemini-2.5-pro",
            litellm_params=litellm.CompletionRequest(model="gemini/gemini-2.5-pro"),
        ),
        ModelConfig(
            model_name="gemini-2.5-flash",
            litellm_params=litellm.CompletionRequest(model="gemini/gemini-2.5-flash"),
        ),
        ModelConfig(
            model_name="qwen3-coder-plus",
            litellm_params=litellm.CompletionRequest(
                model="dashscope/qwen3-coder-plus"
            ),
        ),
        ModelConfig(
            model_name="deepseek-reasoner",
            litellm_params=litellm.CompletionRequest(
                model="deepseek/deepseek-reasoner"
            ),
        ),
        ModelConfig(
            model_name="deepseek-chat",
            litellm_params=litellm.CompletionRequest(model="deepseek/deepseek-chat"),
        ),
    ]
    default_litellm_params: dict[str, Any] = {
        "stream_timeout": 30.0,
        "timeout": 300.0,
    }
    context_window_fallbacks: list[dict[str, list[str]]] = [
        {"deepseek-chat": ["qwen3-coder-plus"]},
        {"deepseek-reasoner": ["qwen3-coder-plus"]},
    ]

    def build(self) -> litellm.Router:
        return litellm.Router(**self.model_dump())


class LLMConfig(ps.BaseSettings):
    model: str | None = None
    router: RouterConfig = RouterConfig()

    @override
    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[ps.BaseSettings],
        init_settings: ps.PydanticBaseSettingsSource,
        env_settings: ps.PydanticBaseSettingsSource,
        dotenv_settings: ps.PydanticBaseSettingsSource,
        file_secret_settings: ps.PydanticBaseSettingsSource,
    ) -> tuple[ps.PydanticBaseSettingsSource, ...]:
        sources: Sequence[ps.PydanticBaseSettingsSource] = (
            super().settings_customise_sources(
                settings_cls,
                init_settings,
                env_settings,
                dotenv_settings,
                file_secret_settings,
            )
        )
        dirs: platformdirs.AppDirs = platformdirs.AppDirs(
            appname="liblaf/lime", appauthor="liblaf"
        )
        toml_config = ps.TomlConfigSettingsSource(
            settings_cls,
            toml_file=[cfg / "config.toml" for cfg in dirs.iter_config_paths()],
        )
        return (*sources, toml_config)
