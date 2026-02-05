"""Remove a specific track from the MKV file."""

from __future__ import annotations

from ..operations import RemoveTrack
from .base import Action, ActionContext


class RemoveTrackAction(Action):
    """Remove a specific track from the MKV file."""

    def __init__(self, track_id: int):
        self.track_id = track_id

    def analyze(self, context: ActionContext):
        """Create RemoveTrack operation with the provided track ID."""
        return {v: [RemoveTrack(self.track_id)] for v in context.video_files}
