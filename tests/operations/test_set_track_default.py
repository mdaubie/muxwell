from __future__ import annotations

import pytest
import typer

from muxwell.mkv.models import MKVFile
from muxwell.operations import SetTrackDefault


def test_set_track_default_apply_sets_default_flag(mkv_file: MKVFile):
    SetTrackDefault(0, True).apply(mkv_file)
    assert mkv_file.tracks[0].default_track is True


def test_set_track_default_apply_raises_for_missing_track(mkv_file: MKVFile):
    with pytest.raises(typer.BadParameter) as exc_info:
        SetTrackDefault(10, True).apply(mkv_file)
    assert f"Track 10 not found in file {mkv_file.file_path}" in str(exc_info.value)
