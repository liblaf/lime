import enum
from typing import Any

import cappa
import questionary


class Action(enum.StrEnum):
    CONFIRM = enum.auto()
    EDIT = enum.auto()


async def prompt_action() -> Action:
    answer: Any = await questionary.select(
        message="Commit message generated successfully",
        choices=[
            questionary.Choice("✅  Use this message", value=Action.CONFIRM),
            questionary.Choice("✏️  Edit this message", value=Action.EDIT),
        ],
    ).ask_async()
    if answer is None:
        raise cappa.Exit(code=1)
    return Action(answer)
