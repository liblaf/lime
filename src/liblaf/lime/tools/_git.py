import asyncio
import subprocess
import sys
from collections.abc import Generator, Iterable, Sequence
from pathlib import Path
from typing import Protocol

import attrs
import git
import gitmatch

from liblaf.lime.typing import PathLike, StrOrBytesPath

from .constants import DEFAULT_IGNORES


class GitInfo(Protocol):
    @property
    def domain(self) -> str: ...
    @property
    def owner(self) -> str: ...
    @property
    def repo(self) -> str: ...


@attrs.define
class Git:
    repo: git.Repo = attrs.field(
        factory=lambda: git.Repo(search_parent_directories=True)
    )

    @property
    def root(self) -> Path:
        return Path(self.repo.working_dir)

    async def commit(
        self,
        message: str | None = None,
        *,
        edit: bool = False,
        exit_on_error: bool = False,
    ) -> None:
        cmd: list[StrOrBytesPath] = ["git", "commit"]
        if message:
            cmd.append(f"--message={message}")
        if edit:
            cmd.append("--edit")
        process: asyncio.subprocess.Process = (
            await asyncio.subprocess.create_subprocess_exec(*cmd)
        )
        returncode: int = await process.wait()
        if returncode != 0:
            if exit_on_error:
                sys.exit(returncode)
            raise subprocess.CalledProcessError(returncode, cmd)

    def diff(self, include: Sequence[StrOrBytesPath] = []) -> str:
        args: list[StrOrBytesPath] = [
            "--minimal",
            "--no-ext-diff",
            "--cached",
            "--",
            *include,
        ]
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
        gi: gitmatch.Gitignore[str] = gitmatch.compile(ignore)
        entries: Iterable[PathLike] = [entry for entry, _ in self.repo.index.entries]
        entries = filter_git_lfs(entries, root=self.root)
        for entry in entries:
            path: Path = Path(entry)
            if gi.match(path):
                continue
            if is_binary(self.root, path):
                continue
            if ignore_generated and is_generated(self.root, path):
                continue
            yield path


def filter_git_lfs(entries: Iterable[PathLike], *, root: Path) -> Generator[str]:
    process: subprocess.CompletedProcess[str] = subprocess.run(
        ["git", "check-attr", "filter", "--stdin"],
        stdout=subprocess.PIPE,
        cwd=root,
        check=True,
        input="\n".join(map(str, entries)),
        text=True,
    )
    for line in process.stdout.splitlines():
        path: str
        attribute: str
        info: str
        path, attribute, info = line.rsplit(": ", maxsplit=2)
        assert attribute == "filter"
        if info == "lfs":
            continue
        yield path


def is_binary(root: Path, file: Path) -> bool:
    file: Path = root / file
    try:
        with file.open() as fp:
            for _ in fp:
                pass
    except UnicodeDecodeError:
        return True
    else:
        return False


def is_generated(root: Path, file: Path) -> bool:
    if file.is_relative_to("template"):
        return False
    file = root / file
    if file.stat().st_size > 512_000:  # 500 KB
        return True
    with file.open() as fp:
        for _, line in zip(range(5), fp, strict=False):
            # ref: <https://generated.at/>
            if "@generated" in line:
                return True
    return False
