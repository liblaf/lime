import asyncio

import cappa

from .parse import Lime


def main() -> None:
    asyncio.run(cappa.invoke_async(Lime))


if __name__ == "__main__":
    main()
