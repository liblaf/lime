import asyncio
import os
import subprocess
import tempfile
from pathlib import Path

from .parse import RepomixConfig


async def repomix(config: RepomixConfig, instruction: str | None = None) -> str:
    cmd: list[str | bytes | os.PathLike[str] | os.PathLike[bytes]] = ["repomix"]
    with tempfile.TemporaryDirectory() as tmpdir_str:
        tmpdir: Path = Path(tmpdir_str)
        output: Path = tmpdir / "repomix-output.xml"
        cmd += ["--output", output]
        cmd += ["--style", "xml"]
        if config.compress:
            cmd += ["--compress"]
        if not config.files:
            cmd += ["--no-files"]
        if config.truncate_base64:
            cmd += ["--truncate-base64"]
        if instruction:
            instruction_file: Path = tmpdir / "repomix-instruction.md"
            instruction_file.write_text(instruction)
            cmd += ["--instruction-file-path", instruction_file]
        process: asyncio.subprocess.Process = (
            await asyncio.subprocess.create_subprocess_exec(*cmd)
        )
        returncode: int = await process.wait()
        if returncode != 0:
            raise subprocess.CalledProcessError(returncode, cmd)
        return output.read_text()
