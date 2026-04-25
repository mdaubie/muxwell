from __future__ import annotations

from pathlib import Path

from muxwell.mkv.models import MKVFile
from muxwell.operations import AddSubtitles


def test_add_subtitles_apply_adds_mkvtrack_for_path(mkv_file: MKVFile, subs_file: Path):
    AddSubtitles(subs_file).apply(mkv_file)
    assert mkv_file.tracks[-1].file_path == str(subs_file)
