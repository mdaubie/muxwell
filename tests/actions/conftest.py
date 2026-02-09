"""Shared fixtures for action tests."""

from __future__ import annotations

from typing import TYPE_CHECKING
from unittest.mock import MagicMock

import pytest
from rich.console import Console

from muxwell.actions import ActionContext

if TYPE_CHECKING:
    from pathlib import Path


@pytest.fixture
def empty_dir_action_ctx(tmp_path: Path) -> ActionContext:
    """Create a mock ActionContext with a directory target."""
    context = MagicMock(spec=ActionContext)
    context.target = tmp_path
    context.console = MagicMock(spec=Console)
    context.recursive = False
    context.video_files = []
    context.subtitles_files = []
    return context


@pytest.fixture
def file_action_ctx(temp_video_file: Path) -> ActionContext:
    """Create a mock ActionContext with a file target."""
    context = MagicMock(spec=ActionContext)
    context.target = temp_video_file
    context.console = MagicMock(spec=Console)
    context.recursive = False
    context.video_files = [temp_video_file]
    context.subtitles_files = []
    return context
