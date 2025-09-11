import asyncio

import emoji
import githubkit
import githubkit.versions.latest.models as ghm


async def main(max_description_len: int, n_repos: int) -> None:
    gh: githubkit.GitHub = githubkit.GitHub()
    repos: list[ghm.RepoSearchResultItem] = []
    async for repo in gh.rest.paginate(
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
        print(f"<description>{repo.description}</description>")
        if len(repos) >= n_repos:
            break


if __name__ == "__main__":
    asyncio.run(main(max_description_len=100, n_repos=20))
