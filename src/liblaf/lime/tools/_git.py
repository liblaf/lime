from collections.abc import Generator
from pathlib import Path

import attrs
import git
import giturlparse

from liblaf import grapes


@attrs.define
class GitRepo:
    repo: git.Repo = attrs.field(
        factory=lambda: git.Repo(search_parent_directories=True)
    )

    @property
    def root(self) -> Path:
        return Path(self.repo.working_dir)

    @property
    def info(self) -> grapes.git.GitInfo:
        remote: git.Remote = self.repo.remote()
        return giturlparse.parse(remote.url)  # pyright: ignore[reportReturnType]

    def list_generated_files(self) -> Generator[Path]:
        for file in self.ls_files():
            if file.stat().st_size > 512_000:
                yield file
                continue
            with file.open() as fp:
                for _, line in zip(range(5), fp, strict=False):
                    if "@generated" in line:
                        yield file
                        break

    def ls_files(self) -> list[Path]:
        output: str = self.repo.git.ls_files()
        return [Path(line) for line in output.splitlines() if line]
