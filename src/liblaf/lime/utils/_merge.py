from collections.abc import Mapping
from typing import overload

import pydantic


@overload
def merge[C: pydantic.BaseModel](config: C, /, *configs: C | Mapping) -> C: ...
@overload
def merge(config: Mapping, /, *configs: Mapping) -> Mapping: ...
def merge[C: pydantic.BaseModel](
    config: C | Mapping, /, *configs: C | Mapping
) -> C | Mapping:
    data: Mapping = _as_mapping(config)
    for c in configs:
        data = _merge_binary(data, c)
    if isinstance(config, pydantic.BaseModel):
        return config.model_validate(data)
    return data


def _as_mapping(
    data: pydantic.BaseModel | Mapping,
    *,
    exclude_unset: bool = True,
    exclude_none: bool = True,
) -> Mapping:
    if isinstance(data, pydantic.BaseModel):
        return data.model_dump(exclude_unset=exclude_unset, exclude_none=exclude_none)
    return data


def _merge_binary(
    a: Mapping | pydantic.BaseModel, b: Mapping | pydantic.BaseModel
) -> Mapping:
    a = _as_mapping(a)
    b = _as_mapping(b)
    result = dict(a)
    for key, value in b.items():
        if key in a and isinstance(a[key], Mapping) and isinstance(value, Mapping):
            result[key] = _merge_binary(result[key], value)
        else:
            result[key] = value
    return result
