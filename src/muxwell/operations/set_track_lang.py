"""Set track language operation."""

import typer

from ..mkv import MKVFile
from . import Operation


class SetTrackLanguage(Operation):
    """Set the language of a specific track in an MKV file."""

    def __init__(self, track_id: int, lang: str):
        self.track_id = track_id
        self.lang = lang

    def apply(self, video: MKVFile):
        if track := video.select_track(self.track_id):
            track.language = self.lang
            track.language_ietf = self.lang
        else:
            raise typer.BadParameter(
                f"Track {self.track_id} not found in file {video.file_path}"
            )
