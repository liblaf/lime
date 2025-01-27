import asyncio
from typing import Annotated

import typer
import typer_di

app = typer_di.TyperDI(name="topics")


@app.command()
def main(
    add: Annotated[list[str] | None, typer.Option()] = None,
    n_topics: Annotated[int, typer.Option()] = 10,
) -> None:
    from . import main

    add = add or []
    asyncio.run(main(add=add, n_topics=n_topics))
