"""Tests for muxwell.cli.info module."""

from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from muxwell.cli.app import app

runner = CliRunner()


class TestInfoCommand:
    """Tests for the info command."""

    def test_info_help(self):
        """Test that info command shows help."""
        result = runner.invoke(app, ["info", "--help"])
        assert result.exit_code == 0
        assert "Usage" in result.stdout
        assert "info" in result.stdout

    def test_info_with_nonexistent_path(self, tmp_path: Path):
        """Test info command with non-existent path."""
        nonexistent = tmp_path / "nonexistent"
        result = runner.invoke(app, ["info", str(nonexistent)])
        assert result.exit_code == 2
        assert "Invalid value for '[TARGET]'" in result.stderr

    def test_info_with_empty_directory(self, tmp_path: Path):
        """Test info command with empty directory."""
        result = runner.invoke(app, ["info", str(tmp_path)])
        assert result.exit_code == 0
        assert "No video files found" in result.stdout

    def test_info_with_bracketed_directory_path(self, tmp_path: Path):
        """Test info command prints bracketed directory paths literally."""
        bracketed = tmp_path / "Season [01]"
        bracketed.mkdir()

        result = runner.invoke(app, ["info", str(bracketed)])
        assert result.exit_code == 0
        assert "No video files found" in result.stdout
        assert "Season [01]" in result.stdout

    def test_info_quiet_option(self, tmp_path: Path):
        """Test info command with empty directory and quiet option."""
        result = runner.invoke(app, ["info", str(tmp_path), "--quiet"])
        assert result.exit_code == 0
        assert result.stdout == ""  # No output in quiet mode
