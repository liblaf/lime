from pathlib import Path

import typer


def app_dir() -> Path:
    return Path(typer.get_app_dir("lime"))
