from typing import Annotated

import attrs
from cappa import Arg


@attrs.define(slots=False)
class LLMArgs:
    model: Annotated[str | None, Arg(long=True, default=None, group="LLM")]
    temperature: Annotated[float | None, Arg(long=True, default=None, group="LLM")]
    base_url: Annotated[str | None, Arg(long=True, default=None, group="LLM")]
    api_key: Annotated[str | None, Arg(long=True, default=None, group="LLM")]
