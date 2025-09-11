from pathlib import Path

import jinja2
import litellm

from liblaf.lime import tools
from liblaf.lime.cli.parse import Generate
from liblaf.lime.llm import LLM


async def generate(self: Generate) -> None:
    git: tools.Git = tools.Git()
    llm: LLM = LLM.from_args(self)
    files: list[Path] = list(
        git.ls_files(ignore=self.ignore, default_ignore=self.default_ignore)
    )
    jinja: jinja2.Environment = tools.prompt_templates()
    template: jinja2.Template = jinja.get_template(self.prompt)
    instruction: str = template.render()
    repomix: str = await tools.repomix(
        self, include=files, instruction=instruction, root=git.root
    )
    response: litellm.ModelResponse = await llm.live(
        messages=[{"role": "user", "content": repomix}],
    )
    content: str = litellm.get_content_from_model_response(response)
    print(content)
