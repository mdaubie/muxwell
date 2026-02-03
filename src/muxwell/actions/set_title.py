"""Infer title from filename action."""

from ..operations import SetTitle
from . import Action, ActionContext


class SetTitleAction(Action):
    """Set title"""

    def __init__(self, title: str):
        self.title = title

    def analyze(self, context: ActionContext):
        """Create SetTitle operation with the provided title."""
        return {v: [SetTitle(self.title)] for v in context.video_files}
