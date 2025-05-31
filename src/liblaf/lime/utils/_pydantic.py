import functools
from collections.abc import Mapping
from pathlib import Path
from typing import Self

import platformdirs
import pydantic
import pydantic.alias_generators
import pydantic_settings as ps

from liblaf import grapes
from liblaf.lime import utils
from liblaf.lime.utils._merge import merge


def config_file(filename: str) -> list[Path]:
    dirs = platformdirs.PlatformDirs(appname="liblaf/lime", appauthor="liblaf")
    paths: list[Path] = [Path(filename)]
    paths.extend(path / filename for path in dirs.iter_data_paths())
    return paths


@functools.lru_cache
def load_config[C: pydantic.BaseModel](cls: type[C], name: str) -> C:
    dirs = platformdirs.PlatformDirs(appname="liblaf/lime", appauthor="liblaf")
    paths: list[Path] = []
    for ext in [".json", ".toml", ".yaml", ".yml"]:
        filename: str = f"{name}{ext}"
        paths.append(Path(filename))
        paths.extend(path / filename for path in dirs.iter_config_paths())
    data: list[Mapping] = [grapes.load(path) for path in paths if path.exists()]
    config: C = merge(cls(), *data)
    return config


def to_kebab(s: str) -> str:
    return pydantic.alias_generators.to_snake(s).replace("_", "-")


class BaseModel(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(
        validate_assignment=True,
        validate_default=True,
        validate_return=True,
    )

    def merge(
        self, mapping: Mapping | pydantic.BaseModel | None = None, /, **kwargs
    ) -> Self:
        if mapping is None:
            mapping = {}
        elif isinstance(mapping, pydantic.BaseModel):
            mapping = mapping.model_dump(exclude_unset=True, exclude_none=True)
        mapping = {**mapping, **kwargs}
        return utils.merge(self, mapping)


class BaseSettings(ps.BaseSettings):
    model_config = ps.SettingsConfigDict(
        validate_assignment=True,
        validate_default=True,
        validate_return=True,
    )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[ps.BaseSettings],
        init_settings: ps.PydanticBaseSettingsSource,
        env_settings: ps.PydanticBaseSettingsSource,
        dotenv_settings: ps.PydanticBaseSettingsSource,
        file_secret_settings: ps.PydanticBaseSettingsSource,
    ) -> tuple[ps.PydanticBaseSettingsSource, ...]:
        sources: list[ps.PydanticBaseSettingsSource] = list(
            super().settings_customise_sources(
                settings_cls,
                init_settings,
                env_settings,
                dotenv_settings,
                file_secret_settings,
            )
        )
        sources.extend(
            [
                ps.JsonConfigSettingsSource(settings_cls),
                ps.TomlConfigSettingsSource(settings_cls),
                ps.YamlConfigSettingsSource(settings_cls),
            ]
        )
        return tuple(sources)
