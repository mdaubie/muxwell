"""Shared test fixtures for muxwell tests."""

from __future__ import annotations

from pathlib import Path

import pytest
from pytest import FixtureRequest
from rich.console import Console


@pytest.fixture
def console() -> Console:
    """Return a Rich console for testing."""
    return Console(force_terminal=False, force_jupyter=False)


@pytest.fixture
def video_file(request: FixtureRequest, tmp_path: Path) -> Path:
    """Create a single file based on the test parameter.

    Args:
        param: String specifying file type:
            - 'existent': Creates a regular file in tmp_path
            - 'unexistent': Returns path without creating file
            - 'nested' or 'nested_existent': Creates file in nested directory
            - 'nested_unexistent': Returns nested path without creating file
    """
    param = getattr(request, "param", "existent")
    return _create_video_file(tmp_path, param)


@pytest.fixture
def video_files(request: pytest.FixtureRequest, tmp_path: Path) -> list[Path]:
    """Create files based on the test parameter.

    Args:
        param: Either a string or list of strings specifying file types:
            - 'existent': Creates a regular file in tmp_path
            - 'unexistent': Returns path without creating file
            - 'nested' or 'nested_existent': Creates file in nested directory
            - 'nested_unexistent': Returns nested path without creating file
    """
    param: str | list[str] = getattr(request, "param", ["existent", "existent"])
    if isinstance(param, str):
        param = [param]
    return [_create_video_file(tmp_path, p, i + 1) for i, p in enumerate(param)]


def _create_video_file(
    tmp_path: Path, file_type: str, index: int | None = None
) -> Path:
    """Helper to create a single video file based on file type.

    Args:
        tmp_path: Base temporary directory path
        file_type: Type of file to create ('existent', 'unexistent', 'nested', etc.)
        index: Optional index for unique naming (default: None)

    Returns:
        Path to the created (or non-created) file
    """
    idx = index or ""
    match file_type:
        case "existent":
            path = tmp_path / f"existent{idx}.mkv"
            path.touch()
            return path
        case "unexistent":
            path = tmp_path / f"unexistent{idx}.mkv"
            return path
        case "nested" | "nested_existent":
            nested_dir = tmp_path / "nested"
            nested_dir.mkdir(exist_ok=True)
            path = nested_dir / f"nested_existent{idx}.mkv"
            path.touch()
            return path
        case "nested_unexistent":
            nested_dir = tmp_path / "nested"
            nested_dir.mkdir(exist_ok=True)
            path = nested_dir / f"nested_unexistent{idx}.mkv"
            return path
        case _:
            raise ValueError(f"Invalid parameter value: {file_type}")
