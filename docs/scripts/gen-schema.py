import json
from typing import Any

from mkdocs_gen_files.editor import FilesEditor

from liblaf import lime


def main() -> None:
    editor: FilesEditor = FilesEditor.current()
    schema: dict[str, Any] = lime.Config.model_json_schema()
    with editor.open("schema.json", "w") as fp:
        json.dump(schema, fp)


main()
