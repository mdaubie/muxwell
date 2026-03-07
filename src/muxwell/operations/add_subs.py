"""Add subtitles track operation."""

from __future__ import annotations

from pathlib import Path

from pymkv import MKVTrack

from ..mkv import MKVFile
from .base import Operation, OperationPriority


class AddSubtitles(Operation):
    """Add a subtitles track to an MKV file."""

    priority = OperationPriority.ADD_TRACK

    def __init__(self, path: Path):
        self.path = path

    def apply(self, video: MKVFile):
        video.add_track(MKVTrack(str(self.path)))
