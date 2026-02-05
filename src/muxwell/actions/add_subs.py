"""Action to add a subtitles track to an MKV file."""

from __future__ import annotations

from pathlib import Path

import typer

from ..operations import AddSubtitles
from ..utils.files import SUBTITLES_EXTENSIONS
from .base import Action, ActionContext


class AddSubtitlesAction(Action):
    """Add subtitles track"""

    def __init__(self, path: Path):
        if path.suffix.lower() not in SUBTITLES_EXTENSIONS:
            raise typer.BadParameter(
                f"Unsupported subtitles format: {path.suffix}, supported formats are: {', '.join(SUBTITLES_EXTENSIONS)}"
            )
        self.path = path

    def analyze(self, context: ActionContext):
        """Create AddSubtitles operation with the provided path."""
        return {v: [AddSubtitles(self.path)] for v in context.video_files}
