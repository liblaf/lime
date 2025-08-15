import asyncio
import subprocess
from collections.abc import Generator, Sequence
from pathlib import Path
from typing import cast

import attrs
import git
import giturlparse

from liblaf import grapes
from liblaf.lime.typed import StrOrBytesPath

from .constants import DEFAULT_IGNORES


@attrs.define
class Git:
    repo: git.Repo = attrs.field(
        factory=lambda: git.Repo(search_parent_directories=True)
    )

    @property
    def root(self) -> Path:
        return Path(self.repo.working_dir)

    @property
    def info(self) -> grapes.git.GitInfo:
        remote: git.Remote = self.repo.remote()
        return cast("grapes.git.GitInfo", giturlparse.parse(remote.url))

    async def commit(self, message: str, *, edit: bool = False) -> None:
        cmd: list[StrOrBytesPath] = ["git", "commit", f"--message={message}"]
        if edit:
            cmd.append("--edit")
        process: asyncio.subprocess.Process = (
            await asyncio.subprocess.create_subprocess_exec(*cmd)
        )
        returncode: int = await process.wait()
        if returncode != 0:
            raise subprocess.CalledProcessError(returncode, cmd)

    def diff(self, ignore: Sequence[str] = [], *, default_ignore: bool = True) -> str:
        if default_ignore:
            ignore = [*DEFAULT_IGNORES, *ignore]
        args: list[str] = ["--minimal", "--no-ext-diff", "--cached", "--"]
        args.extend(f":(exclude){pattern}" for pattern in ignore)
        return self.repo.git.diff(*args)

    def ls_files(
        self,
        ignore: Sequence[str] = [],
        *,
        default_ignore: bool = True,
        ignore_generated: bool = True,
    ) -> Generator[Path]:
        if default_ignore:
            ignore = [*DEFAULT_IGNORES, *ignore]
        for pathlike, _ in self.repo.index.entries:
            file: Path = Path(pathlike)
            if any(file.match(pattern) for pattern in ignore):
                continue
            if ignore_generated and is_generated(self.root / file):
                continue
            yield file


def is_generated(file: Path) -> bool:
    if file.stat().st_size > 512_000:  # 500 KB
        return True
    with file.open() as fp:
        for _, line in zip(range(5), fp, strict=False):
            # ref: <https://generated.at/>
            if "@generated" in line:
                return True
    return False
