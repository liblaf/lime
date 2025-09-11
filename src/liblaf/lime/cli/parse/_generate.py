from typing import Annotated

import attrs
import cappa
from cappa import Arg

from liblaf.lime import llm, tools


@cappa.command(invoke="liblaf.lime.cli.invoke.generate")
@attrs.define
class Generate(llm.LLMArgs, tools.RepomixArgs):
    prompt: Annotated[str, Arg()]
