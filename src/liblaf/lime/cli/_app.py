import sys
from typing import Annotated, Any, Literal

import cyclopts

from liblaf import grapes
from liblaf.lime._version import __version__

from . import _commit, _meta

app = cyclopts.App(name="lime", version=__version__)


@app.meta.default
def meta(
    *tokens: Annotated[str, cyclopts.Parameter(show=False, allow_leading_hyphen=True)],
    log_level: Annotated[
        Literal["trace", "debug", "info", "success", "warning", "error", "critical"],
        cyclopts.Parameter(env_var="LOGGING_LEVEL"),
    ] = "warning",
) -> Any:
    grapes.init_logging(level=log_level.upper())
    return app(tokens)


app.command(_commit.commit, name="commit")
app.command(_meta.meta, name="meta")


def main() -> None:
    result: Any = app.meta()
    if isinstance(result, int):
        sys.exit(result)
