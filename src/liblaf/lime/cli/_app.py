from typing import Annotated

import cyclopts

from liblaf import grapes
from liblaf.lime._version import __version__

from . import _commit, _meta

app = cyclopts.App(name="lime", version=__version__)
main: cyclopts.App = app.meta


@app.meta.default
def meta(
    *tokens: Annotated[str, cyclopts.Parameter(show=False, allow_leading_hyphen=True)],
) -> None:
    grapes.init_logging()
    app(tokens)


app.command(_commit.commit, name="commit")
app.command(_meta.meta, name="meta")
