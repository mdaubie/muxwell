"""Fixtures for video file tests."""

from __future__ import annotations

from pathlib import Path

import pytest

from .files import FileFactory


@pytest.fixture
def video_file(request: pytest.FixtureRequest, file_factory: FileFactory) -> Path:
    """Create a single video file based on the test parameter."""
    args = getattr(request, "param", {})
    return file_factory(ext="mkv", name="video", **args)


@pytest.fixture
def video_files(
    request: pytest.FixtureRequest, file_factory: FileFactory
) -> list[Path]:
    """Create multiple video files based on the test parameter."""
    args = getattr(request, "param", [{}, {}])
    return [file_factory(ext="mkv", name=f"video_{i}", **p) for i, p in enumerate(args)]
