import attrs
import cappa
from cappa import Subcommands

from ._commit import Commit


@cappa.command
@attrs.define
class Lime:
    command: Subcommands[Commit]
