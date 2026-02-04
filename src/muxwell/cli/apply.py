from pathlib import Path

import typer
from rich.console import Console

from ..actions import Action, AddSubtitlesAction, SetTitleAction
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
    add_subs: list[Path] = typer.Option(
        [],
        help="Path to subtitles file. Can be used multiple times.",
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
        resolve_path=True,
    ),
    quiet: bool = QuietOption,
):
    """Process the specified video file or all video files in the given directory."""
    console = Console(quiet=quiet)

    actions: list[Action] = []
    if set_title:
        actions.append(SetTitleAction(set_title))

    for sub_path in add_subs:
        actions.append(AddSubtitlesAction(sub_path))

    engine = ProcessingEngine(console)
    plans = engine.plan(target, actions)
    if not plans:
        console.print("[yellow]No changes to apply.[/yellow]")
        raise typer.Exit(0)
    engine.execute(plans)
