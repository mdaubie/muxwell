"""Shared test fixtures for muxwell tests."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from pathlib import Path

    from rich.console import Console


@pytest.fixture
def console() -> Console:
    """Return a Rich console for testing."""
    return Console(force_terminal=False, force_jupyter=False)


@pytest.fixture
def temp_video_file(tmp_path: Path) -> Path:
    """Create a temporary video file path."""
    video = tmp_path / "test_video.mkv"
    video.touch()
    return video


@pytest.fixture
def temp_nested_video_files(tmp_path: Path) -> Path:
    """Create temporary video file in nested directory."""
    nested_dir = tmp_path / "nested"
    nested_dir.mkdir()
    video = nested_dir / "test_video.mkv"
    video.touch()
    return video


@pytest.fixture
def temp_video_files(tmp_path: Path) -> list[Path]:
    """Create multiple temporary video file paths."""
    videos = [
        tmp_path / "video1.mkv",
        tmp_path / "video2.mkv",
        tmp_path / "video3.mp4",
    ]
    for video in videos:
        video.touch()
    return videos
