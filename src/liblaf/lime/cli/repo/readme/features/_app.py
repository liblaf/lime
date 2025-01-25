import asyncio

import typer_di

app = typer_di.TyperDI(name="features")


@app.command()
def main() -> None:
    from . import main

    asyncio.run(main())
