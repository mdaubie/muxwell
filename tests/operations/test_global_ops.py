from __future__ import annotations

from muxwell.mkv.models import MKVFile
from muxwell.operations import SetTitle


def test_set_title_apply_sets_video_title(mkv_file: MKVFile):
    SetTitle("A New Title").apply(mkv_file)
    assert mkv_file.title == "A New Title"
