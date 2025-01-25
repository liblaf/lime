from pathlib import Path

import platformdirs


def app_dir() -> Path:
    return Path(platformdirs.user_config_dir("liblaf/lime"))
