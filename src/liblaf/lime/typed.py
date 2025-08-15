import os

type StrOrBytesPath = str | bytes | os.PathLike[str] | os.PathLike[bytes]
