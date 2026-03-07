"""Remove a track from an MKV file."""

from __future__ import annotations

import typer

from ..mkv import MKVFile, TrackSelector
from .base import Operation, OperationPriority


class RemoveTrack(Operation):
    """Remove a specific track from an MKV file."""

    priority = OperationPriority.REMOVE_TRACK

    def __init__(self, track_selector: TrackSelector):
        self.track_selector = track_selector

    def tie_breaker(self) -> tuple[int, ...]:
        # remove tracks by ID first (descending), then by type/lang selector, to avoid id shifting issues
        if isinstance(self.track_selector, int):
            return (0, -self.track_selector)
        else:
            return (1,)

    def apply(self, video: MKVFile):
        track = video.select_track(self.track_selector)
        if track:
            video.remove_track(video.tracks.index(track))
        else:
            raise typer.BadParameter(
                f"Track {self.track_selector} not found in file {video.file_path}"
            )
