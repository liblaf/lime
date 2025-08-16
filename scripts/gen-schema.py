from pathlib import Path
from typing import Any

import msgspec
from mkdocs_gen_files import FilesEditor

from liblaf import lime

SCHEMA_FILE: Path = Path("schemas/config.json")
EDITOR: FilesEditor = FilesEditor.current()


def main() -> None:
    schema: dict[str, Any] = lime.LLMConfig.model_json_schema()
    buf: bytes = msgspec.json.encode(schema)
    with EDITOR.open("schemas/config.json", "wb") as f:
        f.write(buf)


main()
