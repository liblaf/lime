import os

type PathLike = str | os.PathLike[str]
type StrOrBytesPath = str | bytes | os.PathLike[str] | os.PathLike[bytes]
