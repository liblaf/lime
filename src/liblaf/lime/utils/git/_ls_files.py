import git


def ls_files() -> list[str]:
    repo = git.Repo(search_parent_directories=True)
    stdout: str = repo.git.ls_files()
    return stdout.splitlines()
