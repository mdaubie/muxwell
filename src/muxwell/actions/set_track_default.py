"""Set the default flag of a specific track in the MKV file."""

from __future__ import annotations

from ..operations import SetTrackDefault
from .base import Action, ActionContext


class SetTrackDefaultAction(Action):
    """Set the default flag of a specific track in the MKV file."""

    def __init__(self, track_id: int, default: bool):
        self.track_id = track_id
        self.default = default

    def analyze(self, context: ActionContext):
        """Create SetTrackDefault operation with the provided flag."""
        return {
            v: [SetTrackDefault(self.track_id, self.default)]
            for v in context.video_files
        }
