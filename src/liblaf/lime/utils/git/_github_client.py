import asyncio.subprocess as asp
import os

import githubkit


async def make_github_client() -> githubkit.GitHub:
    token: str | None = (
        os.getenv("GH_TOKEN") or os.getenv("GITHUB_TOKEN") or await gh_auth_token()
    )
    gh = githubkit.GitHub(token)
    return gh


async def gh_auth_token() -> str:
    proc: asp.Process = await asp.create_subprocess_exec(
        "gh", "auth", "token", stdout=asp.PIPE
    )
    assert proc.stdout is not None
    stdout: bytes = await proc.stdout.read()
    text: str = stdout.decode()
    token: str = text.strip()
    return token
