from typing import Annotated

import cyclopts
import jinja2
import litellm

from liblaf.lime import llm, prompts, tools, utils


class CompletionRequest(llm.CompletionRequest):
    temperature: float | None = 0.0


async def commit(
    *,
    completion: Annotated[
        CompletionRequest, cyclopts.Parameter(name="*", group="Completion")
    ] = CompletionRequest(),  # noqa: B008
    repomix: Annotated[
        tools.Repomix, cyclopts.Parameter(name="*", group="Repomix")
    ] = tools.Repomix(),  # noqa: B008
    type_: Annotated[str | None, cyclopts.Parameter(name="type")] = None,
) -> None:
    cfg: llm.LiteLLMConfig = llm.litellm_config()
    cfg.completion = utils.merge(cfg.completion, completion)
    template: jinja2.Template = prompts.get_prompt("commit")
    git = tools.Git()
    diff: str = git.diff()
    repomix.instruction = template.render({"DIFF": diff, "TYPE": type_})
    prompt: str = await repomix.run()
    stream: litellm.CustomStreamWrapper = await cfg.acompletion(prompt=prompt)
    response: litellm.ModelResponse = await llm.live(stream)
    message: str = utils.extract_between_tags(response, tag="answer")
    await git.commit(message=message)
