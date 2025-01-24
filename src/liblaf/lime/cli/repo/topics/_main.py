import githubkit
from rich.prompt import Confirm

from liblaf import lime


async def main() -> None:
    instruction: lime.Prompt = lime.get_prompt("topics")
    prompt: str = await lime.plugin.repomix(instruction.prompt)
    topics_str: str = await lime.live([{"role": "user", "content": prompt}])
    confirm: bool = Confirm.ask("Do you want to add these topics to the repo?")
    if confirm:
        topics: list[str] = [topic.strip() for topic in topics_str.split(",")]
        gh: githubkit.GitHub = await lime.make_github_client()
        owner: str
        repo: str
        owner, repo = lime.github_owner_repo()
        await gh.rest.repos.async_replace_all_topics(owner, repo, names=topics)
