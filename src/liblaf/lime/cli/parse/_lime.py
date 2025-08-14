import attrs
import cappa

from liblaf.lime import tools


@cappa.command(invoke="liblaf.lime.cli.invoke.lime")
@attrs.define
class Lime(tools.RepomixConfig): ...
