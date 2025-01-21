import asyncio
from typing import Annotated

import typer

from liblaf import lime


async def async_main(q: str) -> None:
    topics: list[str] = [topic.name async for topic in lime.plugin.github_topics(q=q)]
    topics.sort()
    print(", ".join(topics))


app = typer.Typer()


@app.command()
def main(q: Annotated[str, typer.Option()] = "is:featured") -> None:
    asyncio.run(async_main(q=q))


if __name__ == "__main__":
    app()
