import attrs
import cappa
from cappa import Subcommands

from ._commit import Commit
from ._generate import Generate
from ._repomix import Repomix


@cappa.command
@attrs.define
class Lime:
    command: Subcommands[Commit | Generate | Repomix]
