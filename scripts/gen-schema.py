from pathlib import Path
from typing import Any

import msgspec

from liblaf import lime

SCHEMA_FILE: Path = Path("schemas/config.json")


def main() -> None:
    schema: dict[str, Any] = lime.LLMConfig.model_json_schema()
    buf: bytes = msgspec.json.encode(schema)
    SCHEMA_FILE.parent.mkdir(parents=True, exist_ok=True)
    SCHEMA_FILE.write_bytes(buf)


if __name__ == "__main__":
    main()
