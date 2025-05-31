import sys
from typing import Annotated, Any

import cyclopts

from liblaf import grapes
from liblaf.lime._version import __version__

from . import _commit, _meta

app = cyclopts.App(name="lime", version=__version__)


@app.meta.default
def meta(
    *tokens: Annotated[str, cyclopts.Parameter(show=False, allow_leading_hyphen=True)],
) -> Any:
    grapes.init_logging()
    return app(tokens)


app.command(_commit.commit, name="commit")
app.command(_meta.meta, name="meta")


def main() -> None:
    result: Any = app.meta()
    if isinstance(result, int):
        sys.exit(result)
