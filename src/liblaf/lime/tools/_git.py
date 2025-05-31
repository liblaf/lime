import asyncio
import subprocess
from collections.abc import Generator, Iterable
from pathlib import Path

import git

DEFAULT_IGNORE: list[str] = [
    "**/.cspell.json",
    "**/*-lock.*",
    "**/*.lock",
    "**/CHANGELOG.md",
]


class Git:
    repo: git.Repo

    def __init__(self) -> None:
        self.repo = git.Repo(search_parent_directories=True)

    async def commit(self, message: str) -> None:
        args: list[str] = [
            "git",
            "commit",
            f"--message={message}",
            "--verify",
            "--edit",
        ]
        proc: asyncio.subprocess.Process = await asyncio.create_subprocess_exec(*args)
        returncode: int = await proc.wait()
        if returncode != 0:
            raise subprocess.CalledProcessError(returncode=returncode, cmd=args)

    def diff(
        self,
        ignore: Iterable[str] = [],
        *,
        ignore_default: Iterable[str] = DEFAULT_IGNORE,
        ignore_generated: bool = True,
    ) -> str:
        args: list[str] = ["--no-ext-diff", "--cached"]
        # ref: <https://git-scm.com/docs/gitglossary#Documentation/gitglossary.txt-aiddefpathspecapathspec>
        ignore = list(ignore)
        ignore.extend(ignore_default)
        if ignore_generated:
            ignore.extend(str(file) for file in self.list_generated_files())
        args.extend([f":(glob,exclude){pattern}" for pattern in ignore if pattern])
        return self.repo.git.diff(*args)

    def list_generated_files(self) -> Generator[Path]:
        for file in self.ls_files():
            if file.is_relative_to("template/"):  # skip copier template files
                continue
            with file.open("r") as fp:
                for _, line in zip(range(5), fp, strict=False):
                    if "@generated" in line:
                        yield file
                        break

    def ls_files(self) -> list[Path]:
        output: str = self.repo.git.ls_files()
        return [Path(file) for file in output.splitlines()]
