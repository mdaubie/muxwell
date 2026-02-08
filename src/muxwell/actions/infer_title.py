"""Infer title from filename action."""

from __future__ import annotations

from pathlib import Path

from muxwell.titles import infer_title

from ..operations import SetTitle
from . import Action, ActionContext


class InferTitleAction(Action):
    """Infer title"""

    def analyze(self, context: ActionContext):
        """Create SetTitle operation with the provided title."""
        ops: dict[Path, list[SetTitle]] = {}
        for video in context.video_files:
            if title := infer_title(video):
                ops[video] = [SetTitle(title)]
            else:
                context.console.print(
                    f"[yellow]Could not infer title for {video.name}[/yellow]"
                )
        return ops
