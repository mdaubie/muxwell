from __future__ import annotations

import pytest
import typer
from typer.testing import CliRunner

from muxwell.cli.utils import MutuallyExclusiveGroup

runner = CliRunner()


class TestMutuallyExclusiveGroup:
    """Tests for MutuallyExclusiveGroup callback factory."""

    def test_single_option_with_value_allowed(self):
        """Test that a single option with a value is allowed."""
        app = typer.Typer()
        exclusive_callback = MutuallyExclusiveGroup()

        def cmd(
            option1: str | None = typer.Option(None, callback=exclusive_callback),
        ):
            typer.echo(f"option1: {option1}")

        app.command()(cmd)

        result = runner.invoke(app, ["--option1", "value1"])
        assert result.exit_code == 0
        assert "option1: value1" in result.stdout

    def test_two_mutually_exclusive_options_raises_error(self):
        """Test that setting two mutually exclusive options raises an error."""
        app = typer.Typer()
        exclusive_callback = MutuallyExclusiveGroup()

        def cmd(
            option1: str | None = typer.Option(None, callback=exclusive_callback),
            option2: str | None = typer.Option(None, callback=exclusive_callback),
        ):
            typer.echo(f"option1: {option1}, option2: {option2}")

        app.command()(cmd)

        result = runner.invoke(app, ["--option1", "value1", "--option2", "value2"])
        assert result.exit_code == 2
        assert "mutually exclusive" in result.stderr

    def test_error_message_contains_option_names(self):
        """Test that the error message contains both option names."""
        app = typer.Typer()
        exclusive_callback = MutuallyExclusiveGroup()

        def cmd(
            first_opt: str | None = typer.Option(
                None, "--first-opt", callback=exclusive_callback
            ),
            second_opt: str | None = typer.Option(
                None, "--second-opt", callback=exclusive_callback
            ),
        ):
            pass

        app.command()(cmd)

        result = runner.invoke(app, ["--first-opt", "val1", "--second-opt", "val2"])
        assert result.exit_code == 2
        assert "second_opt" in result.stderr
        assert "first_opt" in result.stderr

    def test_none_value_allowed(self):
        """Test that None values don't trigger mutual exclusivity."""
        app = typer.Typer()
        exclusive_callback = MutuallyExclusiveGroup()

        def cmd(
            option1: str | None = typer.Option(None, callback=exclusive_callback),
            option2: str | None = typer.Option(None, callback=exclusive_callback),
        ):
            typer.echo("success")

        app.command()(cmd)

        # No options provided - both will be None
        result = runner.invoke(app, [])
        assert result.exit_code == 0
        assert "success" in result.stdout

    def test_false_value_allowed_for_bool(self):
        """Test that False values don't trigger mutual exclusivity."""
        app = typer.Typer()
        exclusive_callback = MutuallyExclusiveGroup()

        def cmd(
            option1: bool = typer.Option(False, callback=exclusive_callback),
            option2: str | None = typer.Option(None, callback=exclusive_callback),
        ):
            typer.echo(f"option1: {option1}, option2: {option2}")

        app.command()(cmd)

        # option1 defaults to False, only option2 is set
        result = runner.invoke(app, ["--option2", "value2"])
        assert result.exit_code == 0

    def test_integer_values(self):
        """Test mutual exclusivity with integer values."""
        app = typer.Typer()
        exclusive_callback = MutuallyExclusiveGroup()

        def cmd(
            option1: int | None = typer.Option(None, callback=exclusive_callback),
            option2: int | None = typer.Option(None, callback=exclusive_callback),
        ):
            typer.echo(f"option1: {option1}, option2: {option2}")

        app.command()(cmd)

        result = runner.invoke(app, ["--option1", "42", "--option2", "99"])
        assert result.exit_code == 2
        assert "mutually exclusive" in result.stderr

    def test_single_integer_value_allowed(self):
        """Test that a single integer option works correctly."""
        app = typer.Typer()
        exclusive_callback = MutuallyExclusiveGroup()

        def cmd(
            option1: int | None = typer.Option(None, callback=exclusive_callback),
        ):
            typer.echo(f"option1: {option1}")

        app.command()(cmd)

        result = runner.invoke(app, ["--option1", "42"])
        assert result.exit_code == 0
        assert "option1: 42" in result.stdout

    def test_multiple_independent_groups(self):
        """Test that multiple independent groups work correctly."""
        app = typer.Typer()
        group1_callback = MutuallyExclusiveGroup()
        group2_callback = MutuallyExclusiveGroup()

        def cmd(
            option1: str | None = typer.Option(None, callback=group1_callback),
            option2: str | None = typer.Option(None, callback=group1_callback),
            option3: str | None = typer.Option(None, callback=group2_callback),
            option4: str | None = typer.Option(None, callback=group2_callback),
        ):
            typer.echo("success")

        app.command()(cmd)

        # Setting one option from each group should work
        result = runner.invoke(app, ["--option1", "val1", "--option3", "val3"])
        assert result.exit_code == 0
        assert "success" in result.stdout

    def test_multiple_independent_groups_one_violates(self):
        """Test that violation in one group raises error even if other group is valid."""
        app = typer.Typer()
        group1_callback = MutuallyExclusiveGroup()
        group2_callback = MutuallyExclusiveGroup()

        def cmd(
            option1: str | None = typer.Option(None, callback=group1_callback),
            option2: str | None = typer.Option(None, callback=group1_callback),
            option3: str | None = typer.Option(None, callback=group2_callback),
        ):
            pass

        app.command()(cmd)

        # Group 1 violates, group 2 is fine
        result = runner.invoke(
            app, ["--option1", "val1", "--option2", "val2", "--option3", "val3"]
        )
        assert result.exit_code == 2
        assert "mutually exclusive" in result.stderr

    @pytest.mark.parametrize(
        "args,should_pass",
        [
            (["--option1", "val1"], True),
            (["--option1", "val1", "--option2", "val2"], False),
            (["--option1", "val1", "--option3", "val3"], False),
            (["--option2", "val2", "--option3", "val3"], False),
        ],
    )
    def test_three_options_in_group(self, args: list[str], should_pass: bool):
        """Test that mutual exclusivity works with more than 2 options."""
        app = typer.Typer()
        exclusive_callback = MutuallyExclusiveGroup()

        def cmd(
            option1: str | None = typer.Option(None, callback=exclusive_callback),
            option2: str | None = typer.Option(None, callback=exclusive_callback),
            option3: str | None = typer.Option(None, callback=exclusive_callback),
        ):
            typer.echo("success")

        app.command()(cmd)

        result = runner.invoke(app, args)
        if should_pass:
            assert result.exit_code == 0
            assert "success" in result.stdout
        else:
            assert result.exit_code == 2
            assert "mutually exclusive" in result.stderr

    @pytest.mark.parametrize(
        "args",
        [
            ["--option1", "val1", "--option2", "val2"],
            ["--option2", "val2", "--option1", "val1"],
        ],
    )
    def test_order_independence(self, args: list[str]):
        """Test that the order of options doesn't matter."""
        app = typer.Typer()
        exclusive_callback = MutuallyExclusiveGroup()

        def cmd(
            option1: str | None = typer.Option(None, callback=exclusive_callback),
            option2: str | None = typer.Option(None, callback=exclusive_callback),
        ):
            pass

        app.command()(cmd)

        result = runner.invoke(app, args)
        assert result.exit_code == 2
        assert "mutually exclusive" in result.stderr

    @pytest.mark.parametrize(
        "args,should_pass,expected_output",
        [
            (["--flag1", "--flag2"], False, ""),
            (["--flag1"], True, "flag1: True"),
        ],
    )
    def test_bool_flags(self, args: list[str], should_pass: bool, expected_output: str):
        """Test mutual exclusivity with boolean flags."""
        app = typer.Typer()
        exclusive_callback = MutuallyExclusiveGroup()

        def cmd(
            flag1: bool = typer.Option(False, "--flag1", callback=exclusive_callback),
            flag2: bool = typer.Option(False, "--flag2", callback=exclusive_callback),
        ):
            typer.echo(f"flag1: {flag1}, flag2: {flag2}")

        app.command()(cmd)

        result = runner.invoke(app, args)
        if should_pass:
            assert result.exit_code == 0
            assert expected_output in result.stdout
        else:
            assert result.exit_code == 2
            assert "mutually exclusive" in result.stderr
