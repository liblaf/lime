import githubkit
from rich.prompt import Confirm

from liblaf import lime


async def main() -> None:
    instruction: lime.Prompt = lime.get_prompt("description")
    prompt: str = await lime.plugin.repomix(instruction.prompt)
    description: str = await lime.live([{"role": "user", "content": prompt}])
    confirm: bool = Confirm.ask("Do you want to set this description for the repo?")
    if confirm:
        gh: githubkit.GitHub = await lime.make_github_client()
        owner: str
        repo: str
        owner, repo = lime.github_owner_repo()
        await gh.rest.repos.async_update(owner, repo, description=description)
