from typing import Annotated

import attrs
from cappa import Arg


@attrs.define
class RepomixConfig:
    compress: Annotated[bool, Arg(long=["--compress", "--no-compress"], default=False)]
    files: Annotated[bool, Arg(long=["--files", "--no-files"], default=True)]
    truncate_base64: Annotated[
        bool, Arg(long=["--truncate-base64", "--no-truncate-base64"], default=True)
    ]
