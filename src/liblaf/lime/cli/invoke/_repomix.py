from pathlib import Path

from liblaf.lime import tools
from liblaf.lime.cli.parse import Repomix


async def repomix(self: Repomix) -> None:
    git: tools.Git = tools.Git()
    files: list[Path] = list(
        git.ls_files(ignore=self.ignore, default_ignore=self.default_ignore)
    )
    instruction: str | None = None
    if self.instruction:
        instruction = self.instruction
    elif self.instruction_file:
        instruction = self.instruction_file.read_text()
    repomix: str = await tools.repomix(
        self, include=files, instruction=instruction, root=git.root
    )
    self.output.write_text(repomix)
