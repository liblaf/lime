import asyncio.subprocess as asp
import os
import subprocess as sp
from collections.abc import Sequence
from typing import IO


async def run(
    args: Sequence[str | bytes | os.PathLike[str] | os.PathLike[bytes]],
    *,
    stdin: int | IO | None = None,
    stdout: int | IO | None = None,
    stderr: int | IO | None = None,
    check: bool = True,
) -> asp.Process:
    proc: asp.Process = await asp.create_subprocess_exec(
        *args, stdin=stdin, stdout=stdout, stderr=stderr
    )
    returncode: int = await proc.wait()
    if check and returncode != 0:
        raise sp.CalledProcessError(returncode, args)
    return proc
