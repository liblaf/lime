from collections.abc import Sequence

import githubkit
import litellm
from rich.prompt import Confirm

from liblaf import lime


async def main(add: Sequence[str], n_topics: int) -> None:
    n_topics -= len(add)
    prompt: lime.Prompt = lime.get_prompt("topics")
    messages: list[litellm.AllMessageValues] = prompt.substitiute(
        {"N_TOPICS": str(n_topics)}
    )
    instruction: str = messages[1]["content"]  # pyright: ignore[reportAssignmentType, reportTypedDictNotRequiredAccess]
    messages[1]["content"] = await lime.plugin.repomix(instruction)
    topics_str: str = await lime.live(messages)
    confirm: bool = Confirm.ask("Do you want to add these topics to the repo?")
    if confirm:
        topics: list[str] = [topic.strip() for topic in topics_str.split(",")]
        topics.extend(add)
        gh: githubkit.GitHub = await lime.make_github_client()
        owner: str
        repo: str
        owner, repo = lime.github_owner_repo()
        await gh.rest.repos.async_replace_all_topics(owner, repo, names=topics)
