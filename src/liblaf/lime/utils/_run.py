import asyncio.subprocess as asp
import os
import subprocess as sp
from collections.abc import Sequence


async def run(
    args: Sequence[str | bytes | os.PathLike[str] | os.PathLike[bytes]],
    *,
    check: bool = True,
) -> asp.Process:
    proc: asp.Process = await asp.create_subprocess_exec(*args)
    returncode: int = await proc.wait()
    if check and returncode != 0:
        raise sp.CalledProcessError(returncode, args)
    return proc
