"""Set the language of a specific track in the MKV file."""

from __future__ import annotations

from ..operations import SetTrackLanguage
from ..utils.lang import normalize_language
from .base import Action, ActionContext


class SetTrackLanguageAction(Action):
    """Set the language of a specific track in the MKV file."""

    def __init__(self, track_id: int, lang: str):
        self.track_id = track_id
        self.lang = normalize_language(lang)

    def analyze(self, context: ActionContext):
        """Create SetTrackLanguage operation with the provided language."""
        return {
            v: [SetTrackLanguage(self.track_id, self.lang)] for v in context.video_files
        }
