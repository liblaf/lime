import githubkit
import litellm
from rich.prompt import Confirm

from liblaf import lime


async def main(max_len: int) -> None:
    prompt: lime.Prompt = lime.get_prompt("description")
    messages: list[litellm.AllMessageValues] = prompt.substitiute(
        {"MAX_LEN": str(max_len)}
    )
    instruction: str = messages[1]["content"]  # pyright: ignore[reportAssignmentType, reportTypedDictNotRequiredAccess]
    messages[1]["content"] = await lime.plugin.repomix(instruction)
    description: str = await lime.live(messages)
    confirm: bool = Confirm.ask("Do you want to set this description for the repo?")
    if confirm:
        gh: githubkit.GitHub = await lime.make_github_client()
        owner: str
        repo: str
        owner, repo = lime.github_owner_repo()
        await gh.rest.repos.async_update(owner, repo, description=description)
