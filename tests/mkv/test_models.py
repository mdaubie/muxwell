"""Tests for muxwell.mkv.models module."""

# pyright: reportPrivateUsage=false

from __future__ import annotations

from pathlib import Path

from pymkv import MKVTrack

from muxwell.mkv.models import MKVFile


class TestMKVFileChanged:
    def test_unchanged_after_init(self, mkv_file: MKVFile):
        """A freshly loaded MKVFile reports no changes."""
        assert not mkv_file.changed

    def test_changed_after_title_update(self, mkv_file: MKVFile):
        mkv_file.title = "New Title"
        assert mkv_file.changed

    def test_changed_when_track_list_length_differs(self, mkv_file: MKVFile):
        """Removing a track (changing track count) is detected as a change."""
        mkv_file.tracks = []
        assert mkv_file.changed

    def test_changed_when_track_filepath_differs(
        self, mkv_file: MKVFile, srt_file: Path, nested_srt_files: list[Path]
    ):
        """Replacing a track with identical metadata but a different source file is detected as a change.

        This is the core regression: remove + add_subs with the same lang/name/codec
        must still be flagged as changed because the track content differs.
        """
        original_track = MKVTrack(srt_file.as_posix())
        mkv_file.tracks = [original_track]
        mkv_file._snapshot = mkv_file.info
        assert not mkv_file.changed

        # Simulate: remove original track, add new track with same metadata but different file
        replacement_track = MKVTrack(nested_srt_files[1].as_posix())
        mkv_file.tracks = [replacement_track]

        assert mkv_file.changed

    def test_not_changed_when_same_track_filepath(
        self, mkv_file: MKVFile, srt_file: Path
    ):
        """A track replacement with the exact same source file is NOT flagged as changed."""
        track = MKVTrack(srt_file.as_posix())
        mkv_file.tracks = [track]
        mkv_file._snapshot = mkv_file.info

        same_track = MKVTrack(srt_file.as_posix())
        mkv_file.tracks = [same_track]

        assert not mkv_file.changed
