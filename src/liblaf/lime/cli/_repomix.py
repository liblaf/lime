from pathlib import Path
from typing import Annotated

from cyclopts import Parameter

from liblaf.lime import tools


async def repomix(
    *,
    instruction: str | None = None,
    instruction_file: Path | None = None,
    output: Path = Path("repomix-output.xml"),
    args: Annotated[tools.RepomixArgs | None, Parameter("*", group="Repomix")] = None,
) -> None:
    if args is None:
        args = tools.RepomixArgs()
    git: tools.Git = tools.Git()
    files: list[Path] = list(
        git.ls_files(ignore=args.ignore, default_ignore=args.default_ignore)
    )
    if instruction_file:
        instruction = instruction_file.read_text()
    repomix: str = await tools.repomix(
        args, include=files, instruction=instruction, root=git.root
    )
    output.write_text(repomix)
