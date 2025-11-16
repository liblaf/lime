import attrs


@attrs.define
class LLMArgs:
    model: str | None = None
    temperature: float | None = None
    base_url: str | None = None
    api_key: str | None = None
