"""Tests for muxwell.cli.apply module."""

from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from muxwell.cli.app import app

runner = CliRunner()


class TestApplyCommand:
    """Tests for the apply command."""

    def test_apply_help(self):
        """Test that apply command shows help."""
        result = runner.invoke(app, ["apply", "--help"])
        assert result.exit_code == 0
        assert "Usage" in result.stdout
        assert "apply" in result.stdout

    def test_apply_with_nonexistent_path(self, tmp_path: Path):
        """Test apply command with non-existent path."""
        nonexistent = tmp_path / "nonexistent"
        result = runner.invoke(app, ["apply", str(nonexistent)])
        assert result.exit_code == 2
        assert "Invalid value for '[TARGET]'" in result.stderr

    def test_apply_with_empty_directory(self, tmp_path: Path):
        """Test apply command with empty directory."""
        result = runner.invoke(
            app, ["apply", str(tmp_path), "--set-title", "Test Title"]
        )
        assert result.exit_code == 0
        assert "No video files found" in result.stdout

    def test_apply_with_bracketed_directory_path(self, tmp_path: Path):
        """Test apply command prints bracketed directory paths literally."""
        bracketed = tmp_path / "Season [01]"
        bracketed.mkdir()

        result = runner.invoke(app, ["apply", str(bracketed), "--rem-track", "0"])
        assert result.exit_code == 0
        assert "No video files found" in result.stdout
        assert "Season [01]" in result.stdout

    def test_apply_quiet_option(self, tmp_path: Path):
        """Test apply command with empty directory and quiet option."""
        result = runner.invoke(app, ["apply", str(tmp_path), "--quiet"])
        assert result.exit_code == 0
        assert result.stdout == ""  # No output in quiet mode

    def test_apply_no_options(self, video_file: Path):
        """Test apply command with no options."""
        result = runner.invoke(app, ["apply", str(video_file)])
        assert result.exit_code == 0
        assert "No changes to apply" in result.stdout

    def test_apply_dry_run_prints_diff_without_muxing(self, video_file: Path):
        """Test apply command dry-run prints planned changes and skips muxing."""
        result = runner.invoke(
            app,
            ["apply", str(video_file), "--set-title", "Test Title", "--dry-run"],
        )

        assert result.exit_code == 0, result.stderr
        assert "Dry run:" in result.stdout
        assert "Title:" in result.stdout
        assert "Test Title" in result.stdout
        assert not Path(f"{video_file}.tmp").exists()
