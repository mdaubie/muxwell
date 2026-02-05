from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import cast

from pymkv import MKVFile as PyMKVFile, MKVTrack as PyMKVTrack


@dataclass
class TrackInfo:
    id: int
    type: str | None
    codec: str | None
    lang: str | None
    name: str | None
    default: bool
    forced: bool


@dataclass
class MkvInfo:
    path: Path
    title: str | None
    tracks: list[TrackInfo]


class MKVFile(PyMKVFile):
    """Extended MKVFile class for additional functionalities."""

    def __init__(self, file_path: str | Path):
        super().__init__(file_path)  # pyright: ignore[reportUnknownMemberType]
        self.file_path = Path(file_path)
        self._snapshot = self.info

    @property
    def info(self) -> MkvInfo:
        """Get structured information about the MKV file."""
        return MkvInfo(
            path=self.file_path,
            title=self.title,
            tracks=[
                TrackInfo(
                    id=track.track_id,
                    type=track.track_type,
                    codec=track.track_codec,
                    lang=track.language,
                    name=track.track_name,
                    default=track.default_track or False,
                    forced=track.forced_track or False,
                )
                for track in self.tracks
            ],
        )

    @property
    def changed(self) -> bool:
        """Check if the MKV file was modified."""
        return self.info != self._snapshot

    def select_track(self, track_id: int) -> PyMKVTrack | None:
        """Get a track by its ID."""
        try:
            return cast(PyMKVTrack, self.get_track(track_id))
        except IndexError:
            return None
