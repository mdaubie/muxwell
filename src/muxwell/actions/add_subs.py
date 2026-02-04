"""Action to add a subtitles track to an MKV file."""

from pathlib import Path

from ..operations import AddSubtitles
from .base import Action, ActionContext


class AddSubtitlesAction(Action):
    """Add subtitles track"""

    def __init__(self, path: Path):
        self.path = path

    def analyze(self, context: ActionContext):
        """Create AddSubtitles operation with the provided path."""
        return {v: [AddSubtitles(self.path)] for v in context.video_files}
