import asyncio.subprocess as asp

import git
import litellm
import typer

from liblaf import lime

PREFIX: str = "<answer>"


async def main(path: list[str], *, verify: bool = True) -> None:
    await lime.run(["git", "status", *path])
    prompt: lime.Prompt = lime.get_prompt("commit")
    repo = git.Repo(search_parent_directories=True)
    diff: str = repo.git.diff("--cached", "--no-ext-diff", *path)
    files: str = repo.git.ls_files()
    messages: list[litellm.AllMessageValues] = prompt.substitiute(
        {"DIFF": diff, "GIT_LS_FILES": files}
    )
    message: str = await lime.live(messages)
    proc: asp.Process = await lime.run(
        [
            "git",
            "commit",
            f"--message={message}",
            "--verify" if verify else "--no-verify",
            "--edit",
        ],
        check=False,
    )
    if proc.returncode:
        raise typer.Exit(proc.returncode)
