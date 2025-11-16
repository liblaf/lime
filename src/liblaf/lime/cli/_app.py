import logging
from typing import Annotated

import cyclopts
from cyclopts import Parameter

from liblaf import grapes
from liblaf.lime._version import __version__

app = cyclopts.App(name="lime", version=__version__)
app.command("liblaf.lime.cli:commit")
app.command("liblaf.lime.cli:generate")
app.command("liblaf.lime.cli:repomix")


@app.meta.default
def init(
    *tokens: Annotated[str, Parameter(show=False, allow_leading_hyphen=True)],
) -> None:
    grapes.logging.init()
    for name in ("LiteLLM", "LiteLLM Proxy", "LiteLLM Router"):
        logger: logging.Logger = logging.getLogger(name)
        logger.handlers.clear()
        logger.setLevel(logging.WARNING)
    app(tokens)


def main() -> None:
    app.meta()
