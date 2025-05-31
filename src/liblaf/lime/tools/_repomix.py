import asyncio
import os
import subprocess
import tempfile
from pathlib import Path
from typing import Annotated

import cyclopts
import pydantic

from ._git import Git


class Repomix(pydantic.BaseModel):
    model_config = pydantic.ConfigDict()
    # Output Options
    # `compress` seems not to work correctly, so we disable it by default
    compress: bool = False
    files: bool = True
    remove_comments: bool = True
    remove_empty_lines: bool = True
    instruction: Annotated[str | None, cyclopts.Parameter(show=False)] = None
    # Filter Options
    ignore: list[str] = [
        "**/.cspell.json",
        "**/.vscode/",
        "**/*-lock.*",
        "**/*.lock",
        "**/CHANGELOG.md",
        "**/go.sum",
    ]

    ignore_generated: bool = True

    def make_args(
        self, tmpdir: str | os.PathLike[str] | None = None
    ) -> list[str | os.PathLike]:
        args: list[str | os.PathLike] = ["repomix", "--stdout"]
        if self.compress:
            args.append("--compress")
        if not self.files:
            args.append("--no-files")
        if self.remove_comments:
            args.append("--remove-comments")
        if self.remove_empty_lines:
            args.append("--remove-empty-lines")
        if self.instruction:
            assert tmpdir
            instruction_file_path: Path = Path(tmpdir) / "repomix-instruction.md"
            instruction_file_path.write_text(self.instruction)
            args.extend(["--instruction-file-path", instruction_file_path])

        ignore: list[str] = self.ignore.copy()
        if self.ignore_generated:
            git = Git()
            ignore.extend(str(file) for file in git.list_generated_files())
        if ignore:
            args.extend(["--ignore", ",".join(ignore)])
        return args

    async def run(self) -> str:
        with tempfile.TemporaryDirectory() as tmpdir:
            args: list[str | os.PathLike] = self.make_args(tmpdir)
            proc: asyncio.subprocess.Process = await asyncio.create_subprocess_exec(
                *args, stdout=subprocess.PIPE
            )
            assert proc.stdout
            output: bytes = await proc.stdout.read()
            returncode: int = await proc.wait()
            if returncode != 0:
                raise subprocess.CalledProcessError(returncode, cmd=args, output=output)
        return output.decode()
