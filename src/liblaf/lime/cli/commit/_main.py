import asyncio.subprocess as asp
import string

import git
import litellm
import typer

from liblaf import lime


async def main(path: list[str], *, verify: bool = True) -> None:
    await lime.run(["git", "status", *path])
    prompt_template = string.Template(lime.prompt("commit"))
    repo = git.Repo(search_parent_directories=True)
    diff: str = repo.git.diff("--cached", "--no-ext-diff", *path)
    files: str = repo.git.ls_files()
    prompt: str = prompt_template.substitute({"GIT_DIFF": diff, "GIT_FILES": files})
    resp: litellm.ModelResponse = await lime.live(prompt, prefix="<Answer>")
    content: str = litellm.get_content_from_model_response(resp)
    message: str = lime.extract_between_tags(content)
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
