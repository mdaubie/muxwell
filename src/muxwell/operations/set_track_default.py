"""Set track default flag operation."""

from __future__ import annotations

import typer

from ..mkv import MKVFile, TrackSelector
from . import Operation


class SetTrackDefault(Operation):
    """Set the default flag of a specific track in an MKV file."""

    def __init__(self, track_selector: TrackSelector, default: bool):
        self.track_selector = track_selector
        self.default = default

    def apply(self, video: MKVFile):
        if track := video.select_track(self.track_selector):
            track.default_track = self.default
        else:
            raise typer.BadParameter(
                f"Track {self.track_selector} not found in file {video.file_path}"
            )
