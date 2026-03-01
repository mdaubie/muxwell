from __future__ import annotations

from pathlib import Path
from typing import Protocol, TypedDict

import pytest


class FileCreateParams(TypedDict, total=False):
    ext: str
    name: str
    nested: bool
    content: str
    encoding: str
    create: bool


class FileFactory(Protocol):
    def __call__(
        self,
        *,
        ext: str,
        name: str = "sample",
        nested: bool = False,
        content: str = "",
        encoding: str = "utf-8",
        create: bool = True,
    ) -> Path: ...


@pytest.fixture
def file_factory(tmp_path: Path) -> FileFactory:
    def _create(
        *,
        ext: str,
        name: str = "sample",
        nested: bool = False,
        content: str = "",
        encoding: str = "utf-8",
        create: bool = True,
    ) -> Path:
        base = tmp_path / "nested" if nested else tmp_path
        base.mkdir(parents=True, exist_ok=True)

        path = base / f"{name}.{ext.lstrip('.')}"
        if create:
            path.write_text(content, encoding=encoding)
        return path

    return _create
