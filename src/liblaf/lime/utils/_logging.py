# make pyright happy
from loguru import logger
from rich.logging import RichHandler

from liblaf import grapes


def init_logging() -> None:
    grapes.init_logging()
    logger.configure(
        handlers=[
            {
                "sink": RichHandler(console=grapes.logging_console()),
                "filter": {"": "INFO", "liblaf": "DEBUG"},
            }
        ]
    )
