from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console

from ..actions import (
    Action,
    AddSubtitlesAction,
    RemoveTrackAction,
    SetTitleAction,
    SetTrackLanguageAction,
)
from ..engine import ProcessingEngine
from .common import QuietOption, RecursiveOption
from .models import IdLangPair


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
    set_track_lang: list[IdLangPair] = typer.Option(
        [],
        parser=IdLangPair.parse,
        help="Set the language of a specific track in the format <track_id>:<lang>. Can be used multiple times.",
    ),
    rem_track: list[int] = typer.Option(
        [],
        help="Remove a specific track by its ID. Can be used multiple times.",
    ),
    quiet: bool = QuietOption,
    recursive: bool = RecursiveOption,
):
    """Process the specified video file or all video files in the given directory."""
    console = Console(quiet=quiet)

    actions: list[Action] = []
    if set_title:
        actions.append(SetTitleAction(set_title))

    for sub_path in add_subs:
        actions.append(AddSubtitlesAction(sub_path))

    # order desc to avoid ID shifting issues
    for track_id in sorted(rem_track, reverse=True):
        actions.append(RemoveTrackAction(track_id))

    for track_lang in set_track_lang:
        actions.append(SetTrackLanguageAction(track_lang.track_id, track_lang.lang))

    engine = ProcessingEngine(console)
    plans = engine.plan(target, actions, recursive)
    if not plans:
        console.print("[yellow]No changes to apply.[/yellow]")
        raise typer.Exit(0)
    engine.execute(plans)
