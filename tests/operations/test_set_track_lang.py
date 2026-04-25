from __future__ import annotations

import pytest
import typer

from muxwell.mkv.models import MKVFile
from muxwell.operations import SetTrackLanguage


def test_set_track_language_apply_sets_language_and_language_ietf(
    mkv_file_with_subs: MKVFile,
):
    SetTrackLanguage(1, "eng").apply(mkv_file_with_subs)
    track = mkv_file_with_subs.tracks[1]
    assert track.language == "eng"
    assert track.language_ietf == "eng"


def test_set_track_language_apply_raises_for_missing_track(mkv_file: MKVFile):
    with pytest.raises(typer.BadParameter) as exc_info:
        SetTrackLanguage(10, "fra").apply(mkv_file)
    assert f"Track 10 not found in file {mkv_file.file_path}" in str(exc_info.value)
