import asyncio
from typing import Annotated

import typer
import typer_di

app = typer_di.TyperDI(name="description")


@app.command()
def main(max_len: Annotated[int, typer.Option()] = 100) -> None:
    from . import main

    asyncio.run(main(max_len=max_len))
