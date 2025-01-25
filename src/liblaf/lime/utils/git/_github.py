import re
from pathlib import Path

import git

GITHUB_URL_PATTERNS: list[str] = [
    r"https://github\.com/(?P<owner>[^/]+)/(?P<repo>[^/]+)\.git"
]


def repo(*, search_parent_directories: bool = True) -> git.Repo:
    return git.Repo(search_parent_directories=search_parent_directories)


def root() -> Path:
    repo = git.Repo(search_parent_directories=True)
    return Path(repo.working_dir)


def github_owner_repo() -> tuple[str, str]:
    repo = git.Repo(search_parent_directories=True)
    remote: git.Remote = repo.remote()
    for pattern in GITHUB_URL_PATTERNS:
        match: re.Match[str] | None = re.match(pattern, remote.url)
        if not match:
            continue
        owner: str = match.group("owner")
        repo_name: str = match.group("repo")
        repo_name.removesuffix(".git")
        return owner, repo_name
    msg: str = "none of the git remotes configured for this repository point to a known GitHub host."
    raise RuntimeError(msg)
