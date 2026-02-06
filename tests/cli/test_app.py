"""Tests for muxwell.cli.app module."""

from __future__ import annotations

from typer.testing import CliRunner

from muxwell.cli.app import app

runner = CliRunner()


class TestCLIApp:
    """Tests for the CLI application."""

    def test_app_help(self):
        """Test that the app shows help."""
        result = runner.invoke(app, ["--help"])
        assert result.exit_code == 0
        assert "Usage" in result.stdout
        assert "command-line tool" in result.stdout

    def test_app_version(self):
        """Test that the app shows version."""
        result = runner.invoke(app, ["--version"])
        assert result.exit_code == 0
        # Version should be printed

    def test_app_no_args_shows_help(self):
        """Test that running with no args shows help."""
        result = runner.invoke(app)
        assert result.exit_code == 2  # usage error
        assert "Usage" in result.stdout

    def test_info_command_exists(self):
        """Test that info command is registered."""
        result = runner.invoke(app, ["info", "--help"])
        assert result.exit_code == 0
        assert "info" in result.stdout

    def test_apply_command_exists(self):
        """Test that apply command is registered."""
        result = runner.invoke(app, ["apply", "--help"])
        assert result.exit_code == 0
        assert "apply" in result.stdout
