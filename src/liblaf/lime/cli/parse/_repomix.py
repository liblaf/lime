from pathlib import Path
from typing import Annotated

import attrs
import cappa
from cappa import Arg

from liblaf.lime import tools


@cappa.command(invoke="liblaf.lime.cli.invoke.repomix")
@attrs.define(slots=False)
class Repomix(tools.RepomixArgs):
    instruction: Annotated[str | None, Arg(long=True, default=None, group="Repomix")]
    instruction_file: Annotated[
        Path | None, Arg(long=True, default=None, group="Repomix")
    ]
    output: Annotated[
        Path, Arg(long=True, default=Path("repomix-output.xml"), group="Repomix")
    ]
