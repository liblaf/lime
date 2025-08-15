from typing import Self

import attrs
import jinja2
import litellm
import rich
from rich.panel import Panel

from liblaf.lime import tools
from liblaf.lime.cli.parse import Commit
from liblaf.lime.llm import LLM

from ._commit_type import COMMIT_TYPES, CommitType
from ._interactive import Action, prompt_action


@attrs.define
class Inputs:
    type: CommitType | None = None
    scope: str | None = None
    breaking_change: bool | None = None

    @classmethod
    def from_args(cls, args: Commit) -> Self:
        return cls(
            type=COMMIT_TYPES[args.type] if args.type else None,
            scope=args.scope,
            breaking_change=args.breaking_change,
        )


async def commit(self: Commit) -> None:
    git: tools.Git = tools.Git()
    inputs: Inputs = Inputs.from_args(self)
    jinja: jinja2.Environment = tools.prompt_templates()
    llm: LLM = LLM.from_args(self)
    template: jinja2.Template = jinja.get_template("commit.md")

    git_diff: str = git.diff(ignore=self.ignore, default_ignore=self.default_ignore)
    instruction: str = template.render(
        commit_types=COMMIT_TYPES.values(), git_diff=git_diff, inputs=inputs
    )
    repomix: str = await tools.repomix(self, instruction=instruction, git=git)
    response: litellm.ModelResponse = await llm.live(
        messages=[{"role": "user", "content": repomix}],
        parser=_response_parser,
    )

    content: str = litellm.get_content_from_model_response(response)
    content = _response_parser(content)
    rich.print(Panel(content, title=f"🤖 {response.model}", title_align="left"))

    action: Action = await prompt_action()
    match action:
        case Action.CONFIRM:
            await git.commit(message=content, edit=False)
        case Action.EDIT:
            await git.commit(message=content, edit=True)


def _response_parser(content: str) -> str:
    return tools.extract_between_tags(content, "answer", strip=True)
