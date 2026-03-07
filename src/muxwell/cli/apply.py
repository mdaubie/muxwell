from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console

from ..actions import (
    Action,
    AddSubtitlesAction,
    AutoMatchSubs,
    InferTitleAction,
    RemoveTrackAction,
    SetTitleAction,
    SetTrackDefaultAction,
    SetTrackLanguageAction,
)
from ..engine import ProcessingEngine
from .common import QuietOption, RecursiveOption
from .models import IdLangPair
from .utils import MutuallyExclusiveGroup

title_excl_cb = MutuallyExclusiveGroup()


def apply(
    target: Path = typer.Argument(
        Path("."),
        help="Path to the video file or directory containing video files.",
        exists=True,
        readable=True,
        resolve_path=True,
    ),
    set_title: str | None = typer.Option(
        None,
        "--set-title",
        callback=title_excl_cb,
        help="Set the title of the MKV file.",
    ),
    infer_title: bool = typer.Option(
        False,
        callback=title_excl_cb,
        help="Infer the title from the filename and set it.",
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
    auto_match_subs: bool = typer.Option(
        False,
        help="Automatically match and add subtitles files based on filename similarity.",
    ),
    set_track_lang: list[IdLangPair] = typer.Option(
        [],
        parser=IdLangPair.parse,
        help="Set the language of a specific track in the format <track_id>:<lang>. Can be used multiple times.",
    ),
    set_default: list[int] = typer.Option(
        [],
        help="Set the default flag of a specific track by its ID. Can be used multiple times.",
    ),
    unset_default: list[int] = typer.Option(
        [],
        help="Unset the default flag of a specific track by its ID. Can be used multiple times.",
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
    if infer_title:
        actions.append(InferTitleAction())

    for sub_path in add_subs:
        actions.append(AddSubtitlesAction(sub_path))
    if auto_match_subs:
        actions.append(AutoMatchSubs())

    for track_id in rem_track:
        actions.append(RemoveTrackAction(track_id))

    for track_lang in set_track_lang:
        actions.append(SetTrackLanguageAction(track_lang.track_id, track_lang.lang))

    for track_id in set_default:
        actions.append(SetTrackDefaultAction(track_id, True))
    for track_id in unset_default:
        actions.append(SetTrackDefaultAction(track_id, False))

    engine = ProcessingEngine(console)
    plans = engine.plan(target, actions, recursive)
    if not plans:
        console.print("[yellow]No changes to apply.[/yellow]")
        raise typer.Exit(0)
    engine.execute(plans)
