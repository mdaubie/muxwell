"""Shared fixtures package for test modules."""

from __future__ import annotations

from .files import file_factory
from .video import video_file, video_files

__all__ = [
    "file_factory",
    "video_file",
    "video_files",
]
