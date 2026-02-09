"""AutoMatchSubs action."""

from __future__ import annotations

import typer

from ..filenames import parse_filename
from ..operations import AddSubtitles
from .base import Action, ActionContext


class AutoMatchSubs(Action):
    """Automatically match subtitles files to video files based on their filenames and create AddSubtitles operations."""

    def analyze(self, context: ActionContext):
        """Create AddSubtitles operation with the provided path."""
        if context.target.is_file():
            raise typer.BadParameter(
                "auto-match-subs can only be used with directories."
            )
        parsed_videos = {
            path: info
            for path in context.video_files
            if (info := parse_filename(path.name)) is not None
        }
        parsed_subs = {
            path: info
            for path in context.subtitles_files
            if (info := parse_filename(path.name)) is not None
        }
        return {
            video_path: matches
            for video_path, video_info in parsed_videos.items()
            if (
                matches := [
                    AddSubtitles(sub_path)
                    for sub_path, sub_info in parsed_subs.items()
                    if sub_info == video_info
                ]
            )
        }
