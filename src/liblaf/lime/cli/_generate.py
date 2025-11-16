from pathlib import Path
from typing import Annotated

import jinja2
import litellm
from cyclopts import Parameter

from liblaf.lime import tools
from liblaf.lime.llm import LLM, LLMArgs


async def generate(
    prompt: str,
    /,
    *,
    llm_args: Annotated[LLMArgs | None, Parameter("*", group="LLM")] = None,
    repomix_args: Annotated[
        tools.RepomixArgs | None, Parameter("*", group="Repomix")
    ] = None,
) -> None:
    if llm_args is None:
        llm_args = LLMArgs()
    if repomix_args is None:
        repomix_args = tools.RepomixArgs()
    git: tools.Git = tools.Git()
    llm: LLM = LLM.from_args(llm_args)
    files: list[Path] = list(
        git.ls_files(
            ignore=repomix_args.ignore, default_ignore=repomix_args.default_ignore
        )
    )
    jinja: jinja2.Environment = tools.prompt_templates()
    template: jinja2.Template = jinja.get_template(prompt)
    instruction: str = template.render()
    repomix: str = await tools.repomix(
        repomix_args, include=files, instruction=instruction, root=git.root
    )
    response: litellm.ModelResponse = await llm.live(
        messages=[{"role": "user", "content": repomix}]
    )
    content: str = litellm.get_content_from_model_response(response)
    print(content)
