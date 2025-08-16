from typing import Annotated

import attrs
import cappa
from cappa import Arg

from liblaf.lime import llm, tools


@cappa.command(invoke="liblaf.lime.cli.invoke.commit")
@attrs.define(slots=False)
class Commit(llm.LLMArgs, tools.RepomixArgs):
    temperature: Annotated[float | None, Arg(long=True, default=0.0, group="LLM")]

    type: Annotated[str | None, Arg(long=True, default=None, group="Commit")]
    scope: Annotated[str | None, Arg(long=True, default=None, group="Commit")]
    breaking_change: Annotated[
        bool | None,
        Arg(
            long=["--breaking-change", "--no-breaking-change"],
            default=None,
            group="Commit",
        ),
    ]
