from typing import Annotated

import attrs
from cappa import Arg


@attrs.define(slots=False)
class RepomixArgs:
    # Repomix Output Options
    compress: Annotated[
        bool, Arg(long=["--compress", "--no-compress"], default=False, group="Repomix")
    ]
    files: Annotated[
        bool, Arg(long=["--files", "--no-files"], default=True, group="Repomix")
    ]
    truncate_base64: Annotated[
        bool,
        Arg(
            long=["--truncate-base64", "--no-truncate-base64"],
            default=True,
            group="Repomix",
        ),
    ]
    # File Selection Options
    default_ignore: Annotated[
        bool,
        Arg(
            long=["--default-ignore", "--no-default-ignore"],
            default=True,
            group="Repomix",
        ),
    ]
    ignore: Annotated[list[str], Arg(long=True, default=[], group="Repomix")]
    ignore_generated: Annotated[
        bool,
        Arg(
            long=["--ignore-generated", "--no-ignore-generated"],
            default=True,
            group="Repomix",
        ),
    ]
