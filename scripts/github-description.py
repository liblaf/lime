import asyncio

import emoji
import githubkit
import githubkit.versions.latest.models as ghm

from liblaf import lime


async def async_main() -> None:
    gh: githubkit.GitHub = await lime.make_github_client()
    repos: list[ghm.RepoSearchResultItem] = []
    async for repo in gh.paginate(
        gh.rest.search.async_repos,
        map_func=lambda r: r.parsed_data.items,
        q="stars:>1000",
        sort="stars",
        order="desc",
    ):
        if not (repo.description and emoji.is_emoji(repo.description[0])):
            continue
        repos.append(repo)
        print(f"<answer>{repo.description}</answer>")
        if len(repos) >= 100:
            break


def main() -> None:
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
