import importlib
import logging

from loguru import logger
from rich.logging import RichHandler

from liblaf import grapes


def suppress_litellm() -> None:
    importlib.import_module("litellm._logging")
    for name in ["LiteLLM Proxy", "LiteLLM Router", "LiteLLM"]:
        logging.getLogger(name).handlers.clear()


def init_logging() -> None:
    suppress_litellm()
    grapes.init_logging()
    logger.configure(
        handlers=[
            {
                "sink": RichHandler(console=grapes.logging_console()),
                "filter": {
                    "": "INFO",
                    "httpx": "WARNING",
                    "liblaf": "DEBUG",
                    "litellm": "WARNING",
                },
            }
        ]
    )
