"""Tests for muxwell.cli.apply module."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from pytest import MonkeyPatch
from typer.testing import CliRunner

import muxwell.cli.apply as apply_module
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

    def test_apply_without_dry_run_executes_plan(
        self, monkeypatch: MonkeyPatch, tmp_path: Path
    ) -> None:
        """Test apply command executes plans when --dry-run is not set."""
        video_file = tmp_path / "video.mkv"
        video_file.touch()
        calls: dict[str, bool] = {"execute": False, "print_plan": False}

        class FakeEngine:
            def __init__(self, _console: Any) -> None:
                pass

            def plan(
                self, _target: Path, _actions: list[Any], _recursive: bool
            ) -> list[object]:
                return [object()]

            def print_plan(self, _plans: list[object]) -> None:
                calls["print_plan"] = True

            def execute(self, _plans: list[object]) -> None:
                calls["execute"] = True

        monkeypatch.setattr(apply_module, "ProcessingEngine", FakeEngine)

        result = runner.invoke(
            app,
            ["apply", str(video_file), "--set-title", "Test Title"],
        )

        assert result.exit_code == 0, result.stderr
        assert calls["execute"] is True
        assert calls["print_plan"] is False
