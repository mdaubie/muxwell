"""Tests for muxwell.subtitles.models module."""

from __future__ import annotations

from pathlib import Path

import pytest
from pysubs2 import SSAFile
from pysubs2.exceptions import FormatAutodetectionError

from muxwell.subtitles.models import SubFile


class TestSubFile:
    """Tests for the SubFile class."""

    @pytest.mark.parametrize(
        ["subs_file", "sub_format"],
        [
            pytest.param({"ext": "srt", "encoding": "utf-8"}, "srt", id="srt-utf8"),
            pytest.param(
                {"ext": "srt", "encoding": "utf-8-sig"}, "srt", id="srt-utf8-bom"
            ),
            pytest.param({"ext": "srt", "encoding": "latin-1"}, "srt", id="srt-latin1"),
            pytest.param({"ext": "ass", "encoding": "utf-8"}, "ass", id="ass-utf8"),
            pytest.param(
                {"ext": "ass", "encoding": "utf-8-sig"}, "ass", id="ass-utf8-bom"
            ),
            pytest.param({"ext": "ass", "encoding": "latin-1"}, "ass", id="ass-latin1"),
            pytest.param({"ext": "ssa", "encoding": "utf-8"}, "ssa", id="ssa-utf8"),
            pytest.param(
                {"ext": "ssa", "encoding": "utf-8-sig"}, "ssa", id="ssa-utf8-bom"
            ),
            pytest.param({"ext": "ssa", "encoding": "latin-1"}, "ssa", id="ssa-latin1"),
        ],
        indirect=["subs_file"],
    )
    def test_subfile_loading(self, subs_file: Path, sub_format: str):
        sub = SubFile(subs_file)
        assert isinstance(sub, SubFile)
        assert isinstance(sub, SSAFile)
        assert sub.path == subs_file
        assert len(sub) == 3
        assert "café" in sub[2].text
        assert sub.format == sub_format

    def test_subfile_invalid_file(self, invalid_srt_file: Path):
        """Test that SubFile raises an error for invalid files."""
        with pytest.raises(FormatAutodetectionError):
            SubFile(invalid_srt_file)

    def test_subfile_nonexistent_file(self, tmp_path: Path):
        """Test that SubFile raises an error for nonexistent files."""
        nonexistent = tmp_path / "nonexistent.srt"

        with pytest.raises(FileNotFoundError):
            SubFile(nonexistent)
