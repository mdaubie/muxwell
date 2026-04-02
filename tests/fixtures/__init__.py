"""Shared fixtures package for test modules."""

from __future__ import annotations

from .files import file_factory
from .mkv import (
    mkv_file_builder,
    mkv_file_builder_error,
    mkv_file_builder_success,
    mkv_file_builders,
    patch_mkv_file,
    patch_mkv_track,
)
from .subtitles import (
    ass_file,
    invalid_srt_file,
    nested_srt_files,
    srt_file,
    ssa_file,
    subs_file,
    subs_files,
)
from .video import video_file, video_files

__all__ = [
    "file_factory",
    "mkv_file_builder",
    "mkv_file_builder_error",
    "mkv_file_builder_success",
    "mkv_file_builders",
    "patch_mkv_file",
    "patch_mkv_track",
    "ass_file",
    "invalid_srt_file",
    "nested_srt_files",
    "srt_file",
    "ssa_file",
    "subs_file",
    "subs_files",
    "video_file",
    "video_files",
]
