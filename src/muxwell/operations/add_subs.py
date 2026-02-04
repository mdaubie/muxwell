"""Add subtitles track operation."""

from pathlib import Path

from pymkv import MKVTrack

from ..mkv import MKVFile
from .base import Operation


class AddSubtitles(Operation):
    """Add a subtitles track to an MKV file."""

    def __init__(self, path: Path):
        self.path = path

    def apply(self, video: MKVFile):
        video.add_track(MKVTrack(str(self.path)))
