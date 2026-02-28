from __future__ import annotations

from pathlib import Path
from typing import cast

import pysubs2
from pysubs2 import SSAFile

from ..utils.files import get_encoding


class SubFile(SSAFile):
    path: Path

    def __new__(cls, file_path: Path) -> SubFile:
        instance = pysubs2.load(
            file_path.as_posix(), encoding=get_encoding(file_path) or "utf-8"
        )
        instance.__class__ = cls
        instance = cast(SubFile, instance)
        instance.path = file_path
        return instance

    def __init__(self, file_path: Path):
        # __init__ is called after __new__, but the instance is already initialized by pysubs2.load
        pass
