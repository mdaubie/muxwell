from pathlib import Path

import typer
from rich.console import Console

from ..actions import Action, SetTitleAction
from ..engine import ProcessingEngine
from .common import QuietOption


def apply(
    target: Path = typer.Argument(
        Path("."),
        help="Path to the video file or directory containing video files.",
        exists=True,
        readable=True,
        resolve_path=True,
    ),
    set_title: str | None = typer.Option(
        None, "--set-title", help="Set the title of the MKV file."
    ),
    quiet: bool = QuietOption,
):
    """Process the specified video file or all video files in the given directory."""
    console = Console(quiet=quiet)

    actions: list[Action] = []
    if set_title:
        actions.append(SetTitleAction(set_title))

    engine = ProcessingEngine(console)
    plans = engine.plan(target, actions)
    if not plans:
        console.print("[yellow]No changes to apply.[/yellow]")
        raise typer.Exit(0)
    engine.execute(plans)
