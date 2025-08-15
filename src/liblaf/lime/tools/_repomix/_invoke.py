import asyncio
import subprocess
import tempfile
from pathlib import Path

import pydantic
import pydantic.alias_generators

from liblaf.lime.tools._git import Git
from liblaf.lime.typed import StrOrBytesPath

from ._parse import RepomixArgs


class BaseModel(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(
        alias_generator=pydantic.alias_generators.to_camel
    )


class RepomixConfigOutput(BaseModel):
    compress: bool = False
    instruction_file_path: Path | None = None
    files: bool = True
    truncate_base64: bool = True


class RepomixConfig(BaseModel):
    output: RepomixConfigOutput = RepomixConfigOutput()
    include: list[str] = []


async def repomix(
    args: RepomixArgs, *, instruction: str | None = None, git: Git | None = None
) -> str:
    if git is None:
        git = Git()
    config = RepomixConfig(
        output=RepomixConfigOutput(
            compress=args.compress,
            files=args.files,
            truncate_base64=args.truncate_base64,
        ),
        include=[
            str(file)
            for file in git.ls_files(
                ignore=args.ignore,
                default_ignore=args.default_ignore,
                ignore_generated=args.ignore_generated,
            )
        ],
    )
    with tempfile.TemporaryDirectory() as tmpdir_str:
        tmpdir: Path = Path(tmpdir_str)

        cmd: list[StrOrBytesPath] = ["repomix"]

        output: Path = tmpdir / "repomix-output.xml"
        cmd += ["--output", output]

        if instruction:
            instruction_file: Path = tmpdir / "repomix-instruction.md"
            instruction_file.write_text(instruction)
            cmd += ["--instruction-file-path", instruction_file]

        config_file: Path = tmpdir / "repomix.config.json"
        config_file.write_text(config.model_dump_json(exclude_none=True))
        cmd += ["--config", config_file]

        process: asyncio.subprocess.Process = (
            await asyncio.subprocess.create_subprocess_exec(*cmd, cwd=git.root)
        )
        returncode: int = await process.wait()
        if returncode != 0:
            raise subprocess.CalledProcessError(returncode, cmd)
        return output.read_text()
