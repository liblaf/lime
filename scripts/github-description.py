import asyncio
from typing import Annotated

import emoji
import githubkit
import githubkit.versions.latest.models as ghm
import typer

from liblaf import lime


async def async_main(max_description_len: int, n_repos: int) -> None:
    gh: githubkit.GitHub = await lime.make_github_client()
    repos: list[ghm.RepoSearchResultItem] = []
    async for repo in gh.paginate(
        gh.rest.search.async_repos,
        map_func=lambda r: r.parsed_data.items,
        q="stars:>1000",
        sort="stars",
        order="desc",
    ):
        if not (
            repo.description
            and emoji.is_emoji(repo.description[0])
            and len(repo.description) <= max_description_len
        ):
            continue
        repos.append(repo)
        print(f"<answer>{repo.description}</answer>")
        if len(repos) >= n_repos:
            break


def main(
    max_description_len: Annotated[int, typer.Option()] = 100,
    n_repos: Annotated[int, typer.Option()] = 20,
) -> None:
    asyncio.run(async_main(max_description_len=max_description_len, n_repos=n_repos))


if __name__ == "__main__":
    typer.run(main)
