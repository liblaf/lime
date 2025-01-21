from typing import Annotated

import typer

from liblaf import lime


def shared_options(model: Annotated[str | None, typer.Option()] = None) -> None:
    lime.init_logging()
    cfg: lime.Config = lime.get_config()
    if model:
        cfg.completion.model = model
