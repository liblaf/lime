import functools
from typing import Any

import litellm
import pydantic
import pydantic_settings as ps

from liblaf import lime

from . import RouterConfig


class Config(ps.BaseSettings):
    model_config = ps.SettingsConfigDict(toml_file=lime.app_dir() / "config.toml")
    completion: litellm.CompletionRequest = pydantic.Field(
        default_factory=lambda: litellm.CompletionRequest(model="deepseek-chat")
    )
    router: RouterConfig = pydantic.Field(default_factory=RouterConfig)

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[ps.BaseSettings],
        init_settings: ps.PydanticBaseSettingsSource,
        env_settings: ps.PydanticBaseSettingsSource,
        dotenv_settings: ps.PydanticBaseSettingsSource,
        file_secret_settings: ps.PydanticBaseSettingsSource,
    ) -> tuple[ps.PydanticBaseSettingsSource, ...]:
        return (
            init_settings,
            env_settings,
            dotenv_settings,
            file_secret_settings,
            ps.TomlConfigSettingsSource(settings_cls),
        )

    @property
    def completion_kwargs(self) -> dict[str, Any]:
        return self.completion.model_dump(
            exclude_unset=True, exclude_defaults=True, exclude_none=True
        )


@functools.cache
def get_config() -> Config:
    return Config()


@functools.cache
def get_router() -> litellm.Router:
    cfg: Config = get_config()
    return cfg.router.build()
