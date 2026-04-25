from __future__ import annotations

from pathlib import Path

from muxwell.mkv.models import MKVFile
from muxwell.operations import RemoveTrack


def test_remove_track_apply_calls_video_remove_track(mkv_file_with_subs: MKVFile):
    original_video_path = mkv_file_with_subs.file_path
    original_subs_path = str(mkv_file_with_subs.tracks[1].file_path)

    RemoveTrack(1).apply(mkv_file_with_subs)

    assert len(mkv_file_with_subs.tracks) == 1
    assert Path(mkv_file_with_subs.tracks[0].file_path) == original_video_path
    assert all(
        str(track.file_path) != original_subs_path
        for track in mkv_file_with_subs.tracks
    )
