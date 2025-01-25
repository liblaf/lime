import asyncio
from typing import Annotated

import typer
import typer_di

from liblaf import lime

app = typer_di.TyperDI(name="commit")


@app.command()
def main(
    path: Annotated[list[str] | None, typer.Argument()] = None,
    *,
    default_exclude: Annotated[bool, typer.Option()] = True,
    verify: Annotated[bool, typer.Option()] = False,
    _: None = typer_di.Depends(lime.shared_options),
) -> None:
    from . import main

    path: list[str] = path or []
    if default_exclude:
        path += [":!*-lock.*", ":!*.lock*", ":!*.cspell.*"]
    asyncio.run(main(path, verify=verify))
