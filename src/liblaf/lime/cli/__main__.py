import asyncio

import cappa

from liblaf.lime._version import __version__

from .parse import Lime


def main() -> None:
    asyncio.run(cappa.invoke_async(Lime, version=__version__))


if __name__ == "__main__":
    main()
