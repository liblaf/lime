from pathlib import Path
from typing import Annotated

import cyclopts
import jinja2
import litellm

from liblaf.lime import llm, prompts


async def meta(
    task: Annotated[Path, cyclopts.Argument()],
    /,
    *,
    completion: Annotated[
        llm.CompletionRequest, cyclopts.Parameter(name="*", group="Completion")
    ] = llm.CompletionRequest(),  # noqa: B008
) -> None:
    cfg: llm.LiteLLMConfig = llm.litellm_config()
    cfg.completion = cfg.completion.merge(completion)
    template: jinja2.Template = prompts.get_prompt("meta")
    prompt: str = template.render({"TASK": task.read_text()})
    stream: litellm.CustomStreamWrapper = await cfg.acompletion(prompt=prompt)
    response: litellm.ModelResponse = await llm.live(stream)
    content: str = litellm.get_content_from_model_response(response)
    print(content)
