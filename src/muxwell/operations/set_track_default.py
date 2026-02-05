"""Set track default flag operation."""

from __future__ import annotations

import typer

from ..mkv import MKVFile
from . import Operation


class SetTrackDefault(Operation):
    """Set the default flag of a specific track in an MKV file."""

    def __init__(self, track_id: int, default: bool):
        self.track_id = track_id
        self.default = default

    def apply(self, video: MKVFile):
        if track := video.select_track(self.track_id):
            track.default_track = self.default
        else:
            raise typer.BadParameter(
                f"Track {self.track_id} not found in file {video.file_path}"
            )
