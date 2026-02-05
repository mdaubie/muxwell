"""Remove a track from an MKV file."""

from ..mkv import MKVFile
from .base import Operation


class RemoveTrack(Operation):
    """Remove a specific track from an MKV file."""

    def __init__(self, track_id: int):
        self.track_id = track_id

    def apply(self, video: MKVFile):
        video.remove_track(self.track_id)
