"""Tests for muxwell.subtitles.wrapper module."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock

import pytest
from rich.console import Console

from muxwell.subtitles.models import SubFile
from muxwell.subtitles.wrapper import SubWrapper

SUBS_FILE_ARGVALUES = [
    pytest.param({"ext": "srt", "encoding": "utf-8"}, id="srt-utf8"),
    pytest.param({"ext": "srt", "encoding": "utf-8-sig"}, id="srt-utf8-bom"),
    pytest.param({"ext": "srt", "encoding": "latin-1"}, id="srt-latin1"),
    pytest.param({"ext": "ass", "encoding": "utf-8"}, id="ass-utf8"),
    pytest.param({"ext": "ass", "encoding": "utf-8-sig"}, id="ass-utf8-bom"),
    pytest.param({"ext": "ass", "encoding": "latin-1"}, id="ass-latin1"),
    pytest.param({"ext": "ssa", "encoding": "utf-8"}, id="ssa-utf8"),
    pytest.param({"ext": "ssa", "encoding": "utf-8-sig"}, id="ssa-utf8-bom"),
    pytest.param({"ext": "ssa", "encoding": "latin-1"}, id="ssa-latin1"),
]


class TestSubWrapper:
    """Tests for the SubWrapper class."""

    @pytest.fixture
    def wrapper(self, console: Console) -> SubWrapper:
        """Create a SubWrapper instance."""
        return SubWrapper(console)

    def test_subwrapper_initialization(self, console: Console):
        """Test SubWrapper initialization."""
        wrapper = SubWrapper(console)
        assert wrapper.console == console

    @pytest.mark.parametrize(["subs_file"], SUBS_FILE_ARGVALUES, indirect=["subs_file"])
    def test_load_subtitles_single_file(self, wrapper: SubWrapper, subs_file: Path):
        """Test loading a single subtitle file."""
        subtitles = wrapper.load_subtitles([subs_file])

        assert len(subtitles) == 1
        assert isinstance(subtitles[0], SubFile)
        assert subtitles[0].path == subs_file
        assert len(subtitles[0]) == 3

    def test_load_subtitles_multiple_files(
        self, wrapper: SubWrapper, subs_files: list[Path]
    ):
        """Test loading multiple subtitle files."""
        subtitles = wrapper.load_subtitles(subs_files)

        assert len(subtitles) == 3
        for sub in subtitles:
            assert isinstance(sub, SubFile)

    def test_load_subtitles_empty_list(self, wrapper: SubWrapper):
        """Test loading an empty list of files."""
        subtitles = wrapper.load_subtitles([])

        assert subtitles == []

    @pytest.mark.parametrize(["subs_file"], SUBS_FILE_ARGVALUES, indirect=["subs_file"])
    def test_save_subtitles_single_file(self, wrapper: SubWrapper, subs_file: Path):
        """Test saving a single subtitle file."""
        sub = SubFile(subs_file)
        sub.shift(ms=1000)

        codes = wrapper.save_subtitles([sub])

        assert len(codes) == 1
        assert codes[0] == 0  # Success

        # Verify the file was actually saved
        assert subs_file.exists()

        # Reload and verify the shift was saved
        reloaded = SubFile(subs_file)
        assert reloaded[0].start == 2000  # Was 1000, shifted by 1000

    def test_save_subtitles_multiple_files(
        self, wrapper: SubWrapper, subs_files: list[Path]
    ):
        """Test saving multiple subtitle files."""
        subtitles = wrapper.load_subtitles(subs_files)

        # Get original start times
        original_starts = [sub[0].start for sub in subtitles]

        # Modify all subtitles
        for sub in subtitles:
            sub.shift(ms=500)

        codes = wrapper.save_subtitles(subtitles)

        assert len(codes) == len(subs_files)
        assert all(code == 0 for code in codes)  # All should succeed

        # Verify all files were modified
        for i, path in enumerate(subs_files):
            reloaded = SubFile(path)
            assert reloaded[0].start == original_starts[i] + 500

    def test_save_subtitles_empty_list(self, wrapper: SubWrapper):
        """Test saving an empty list of subtitles."""
        codes = wrapper.save_subtitles([])

        assert codes == []

    def test_save_subtitles_preserves_format(
        self, wrapper: SubWrapper, subs_files: list[Path]
    ):
        """Test that saving preserves the original format."""
        subs = [SubFile(path) for path in subs_files]

        for sub in subs:
            sub.shift(ms=100)

        wrapper.save_subtitles(subs)

        # Verify formats are preserved
        for sub, path in zip(subs, subs_files, strict=True):
            assert sub.format == path.suffix[1:]  # Format should match file extension

        # Reload and verify they're still valid
        reloaded_subs = [SubFile(path) for path in subs_files]
        for sub, path in zip(reloaded_subs, subs_files, strict=True):
            assert sub.format == path.suffix[1:]  # Format should match file extension

    def test_save_subtitles_error_displays_bracketed_name(
        self, tmp_path: Path, wrapper: SubWrapper
    ):
        """Bracketed filenames should be shown literally in save error output."""
        sub_path = tmp_path / "Episode [1080p].srt"
        sub_path.write_text(
            "1\n00:00:01,000 --> 00:00:03,000\nFirst subtitle\n", encoding="utf-8"
        )
        sub = SubFile(sub_path)
        sub.save = MagicMock(side_effect=RuntimeError("save failed [disk]"))

        wrapper.console = Console(
            force_terminal=False, force_jupyter=False, record=True
        )
        codes = wrapper.save_subtitles([sub])

        assert codes == [1]
        output = wrapper.console.export_text(styles=False)
        assert "Episode [1080p].srt" in output
        assert "save failed [disk]" in output
