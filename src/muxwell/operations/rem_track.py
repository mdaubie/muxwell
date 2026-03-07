"""Remove a track from an MKV file."""

from __future__ import annotations

from ..mkv import MKVFile
from .base import Operation, OperationPriority


class RemoveTrack(Operation):
    """Remove a specific track from an MKV file."""

    priority = OperationPriority.REMOVE_TRACK

    def __init__(self, track_id: int):
        self.track_id = track_id

    def tie_breaker(self):
        # remove tracks in descending order to avoid shifting
        return (-self.track_id,)

    def apply(self, video: MKVFile):
        video.remove_track(self.track_id)
