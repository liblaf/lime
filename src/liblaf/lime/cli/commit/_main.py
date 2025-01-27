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
    message: str = await lime.live(messages, sanitizer=commit_message_sanitizer)
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


def commit_message_sanitizer(message: str) -> str:
    message: str = lime.extract_between_tags(message)
    lines: list[str] = message.split("\n")
    if len(lines) >= 2 and lines[1].strip():
        lines.insert(1, "")
    message = "\n".join(lines)
    return message
