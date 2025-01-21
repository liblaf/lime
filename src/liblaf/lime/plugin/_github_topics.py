import os
from collections.abc import AsyncGenerator

import githubkit
import githubkit.versions.latest.models as ghm


async def github_topics(
    q: str = "is:featured",
) -> AsyncGenerator[ghm.TopicSearchResultItem]:
    gh = githubkit.GitHub(os.getenv("GH_TOKEN") or os.getenv("GITHUB_TOKEN"))
    async for topic in gh.paginate(
        gh.rest.search.async_topics, map_func=lambda x: x.parsed_data.items, q=q
    ):
        yield topic
