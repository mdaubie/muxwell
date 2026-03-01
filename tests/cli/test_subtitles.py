"""Tests for muxwell.cli.subtitles module."""

from __future__ import annotations

from pathlib import Path

import pytest
from typer.testing import CliRunner

from muxwell.cli.app import app

runner = CliRunner()


class TestSubtitlesCommand:
    """Tests for the subtitles command group."""

    def test_subtitles_help(self):
        """Test that the subtitles command shows help."""
        result = runner.invoke(app, ["subtitles", "--help"])
        assert result.exit_code == 0
        assert "Usage" in result.stdout
        assert "subtitles" in result.stdout

    def test_subtitles_no_args_shows_help(self):
        """Test that running subtitles with no args shows help."""
        result = runner.invoke(app, ["subtitles"])
        assert result.exit_code == 2
        assert "Usage" in result.stdout


class TestShiftCommand:
    """Tests for the shift command."""

    def test_shift_help(self):
        """Test that the shift command shows help."""
        result = runner.invoke(app, ["subtitles", "shift", "--help"])
        assert result.exit_code == 0
        assert "shift" in result.stdout.lower()
        assert "offset" in result.stdout.lower()

    @pytest.mark.parametrize(
        ["subs_file", "offset", "expected_lines"],
        [
            pytest.param(
                {"ext": "srt"},
                1000,
                [
                    "00:00:02,000 --> 00:00:04,000",
                    "00:00:06,000 --> 00:00:08,500",
                    "00:00:11,000 --> 00:00:13,000",
                ],
                id="srt+1000",
            ),
            pytest.param(
                {"ext": "ssa"},
                1000,
                [
                    "0,0:00:02.00,0:00:04.00",
                    "0,0:00:06.00,0:00:08.50",
                    "0,0:00:11.00,0:00:13.00",
                ],
                id="ssa+1000",
            ),
            pytest.param(
                {"ext": "ass"},
                1000,
                [
                    "0:00:02.00,0:00:04.00",
                    "0:00:06.00,0:00:08.50",
                    "0:00:11.00,0:00:13.00",
                ],
                id="ass+1000",
            ),
            pytest.param(
                {"ext": "srt"},
                -1000,
                [
                    "00:00:00,000 --> 00:00:02,000",
                    "00:00:04,000 --> 00:00:06,500",
                    "00:00:09,000 --> 00:00:11,000",
                ],
                id="srt-1000",
            ),
            pytest.param(
                {"ext": "ssa"},
                -1000,
                [
                    "0,0:00:00.00,0:00:02.00",
                    "0,0:00:04.00,0:00:06.50",
                    "0,0:00:09.00,0:00:11.00",
                ],
                id="ssa-1000",
            ),
            pytest.param(
                {"ext": "ass"},
                -1000,
                [
                    "0:00:00.00,0:00:02.00",
                    "0:00:04.00,0:00:06.50",
                    "0:00:09.00,0:00:11.00",
                ],
                id="ass-1000",
            ),
        ],
        indirect=["subs_file"],
    )
    def test_shift_single_file(
        self, subs_file: Path, offset: int, expected_lines: list[str]
    ):
        """Test shifting with a negative offset."""
        result = runner.invoke(
            app, ["subtitles", "shift", str(subs_file), "--", str(offset)]
        )
        assert result.exit_code == 0
        assert "Shifted" in result.stdout

        # Verify the file was shifted backward
        content = subs_file.read_text(encoding="utf-8")
        for line in expected_lines:
            assert line in content

    def test_shift_directory_with_subtitles(self, subs_files: list[Path]):
        """Test shifting all subtitle files in a directory."""
        tmp_path = subs_files[0].parent
        result = runner.invoke(app, ["subtitles", "shift", str(tmp_path), "1000"])
        assert result.exit_code == 0
        assert "3 succeeded" in result.stdout

    def test_shift_directory_recursive(self, nested_srt_files: list[Path]):
        """Test shifting subtitle files recursively."""
        tmp_path = nested_srt_files[0].parent

        result = runner.invoke(
            app, ["subtitles", "shift", str(tmp_path), "1000", "--recursive"]
        )
        assert result.exit_code == 0
        assert "2 succeeded" in result.stdout

    def test_shift_directory_non_recursive(self, nested_srt_files: list[Path]):
        """Test shifting subtitle files non-recursively (default)."""
        tmp_path = nested_srt_files[0].parent

        result = runner.invoke(app, ["subtitles", "shift", str(tmp_path), "1000"])
        assert result.exit_code == 0
        # Should only process 1 file (non-recursive)
        assert "1 succeeded" in result.stdout

    def test_shift_no_subtitles_found(self, tmp_path: Path):
        """Test shifting when no subtitle files are found."""
        result = runner.invoke(app, ["subtitles", "shift", str(tmp_path), "1000"])
        assert result.exit_code == 0
        assert "No subtitle files found" in result.stdout

    def test_shift_quiet_mode(self, subs_file: Path):
        """Test shifting in quiet mode."""
        result = runner.invoke(
            app, ["subtitles", "shift", str(subs_file), "1000", "--quiet"]
        )
        assert result.exit_code == 0
        assert result.stdout == ""  # No output in quiet mode

    def test_shift_invalid_file(self, invalid_srt_file: Path):
        """Test shifting with an invalid subtitle file."""
        result = runner.invoke(
            app, ["subtitles", "shift", str(invalid_srt_file), "1000"]
        )
        # pysubs2 raises an exception for invalid files, which causes exit code 1
        assert result.exit_code == 1
