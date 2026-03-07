"""Remove a specific track from the MKV file."""

from __future__ import annotations

from ..mkv import TrackSelector
from ..operations import RemoveTrack
from .base import Action, ActionContext


class RemoveTrackAction(Action):
    """Remove a specific track from the MKV file."""

    def __init__(self, track_selector: TrackSelector):
        self.track_selector = track_selector

    def analyze(self, context: ActionContext):
        """Create RemoveTrack operation with the provided track selector."""
        return {v: [RemoveTrack(self.track_selector)] for v in context.video_files}
