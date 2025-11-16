from pathlib import Path
from typing import Annotated

import attrs
import jinja2
import litellm
import rich
from cyclopts import Parameter
from rich.panel import Panel
from rich.text import Text

from liblaf.lime import tools
from liblaf.lime.llm import LLM
from liblaf.lime.llm._parse import LLMArgs

from ._commit_type import COMMIT_TYPES, CommitType
from ._interactive import Action, prompt_action


@attrs.define
class Inputs:
    type: CommitType | None = None
    scope: str | None = None
    breaking_change: bool | None = None


async def commit(
    *,
    breaking_change: Annotated[bool | None, Parameter(group="Commit")] = None,
    scope: Annotated[str | None, Parameter(group="Commit")] = None,
    temperature: Annotated[float, Parameter(group="LLM")] = 0.0,
    type_: Annotated[str | None, Parameter("type", group="Commit")] = None,
    llm_args: Annotated[LLMArgs | None, Parameter("*", group="LLM")] = None,
    repomix_args: Annotated[
        tools.RepomixArgs | None, Parameter("*", group="Repomix")
    ] = None,
) -> None:
    if llm_args is None:
        llm_args = LLMArgs(temperature=temperature)
    else:
        llm_args.temperature = temperature
    if repomix_args is None:
        repomix_args = tools.RepomixArgs()
    git: tools.Git = tools.Git()
    inputs: Inputs = Inputs(
        type=COMMIT_TYPES[type_] if type_ else None,
        scope=scope,
        breaking_change=breaking_change,
    )
    jinja: jinja2.Environment = tools.prompt_templates()
    llm: LLM = LLM.from_args(llm_args)
    template: jinja2.Template = jinja.get_template("commit.md")

    files: list[Path] = list(
        git.ls_files(
            ignore=repomix_args.ignore, default_ignore=repomix_args.default_ignore
        )
    )
    git_diff: str = git.diff(include=files)
    if not git_diff:
        await git.commit(exit_on_error=True)
        return
    instruction: str = template.render(
        commit_types=COMMIT_TYPES.values(), git_diff=git_diff, inputs=inputs
    )
    repomix: str = await tools.repomix(
        repomix_args, include=files, instruction=instruction, root=git.root
    )
    response: litellm.ModelResponse = await llm.live(
        messages=[{"role": "user", "content": repomix}],
        parser=_response_parser,
    )

    content: str = litellm.get_content_from_model_response(response)
    content = _response_parser(content)
    rich.print(
        Panel(
            content,
            title=Text(f"🤖 {response.model}", style="bold cyan"),
            title_align="left",
            border_style="cyan",
        )
    )

    action: Action = await prompt_action()
    match action:
        case Action.CONFIRM:
            await git.commit(message=content, edit=False, exit_on_error=True)
        case Action.EDIT:
            await git.commit(message=content, edit=True, exit_on_error=True)


def _response_parser(content: str) -> str:
    return tools.extract_between_tags(content, "answer", strip=True)
