from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console

from ..subtitles import SubWrapper
from ..utils.files import collect_subtitles_files
from .common import QuietOption, RecursiveOption

subtitles = typer.Typer(
    name="subtitles",
    help="Apply changes to subtitles file(s).",
    no_args_is_help=True,
)


@subtitles.command(help="Shift subtitles by a specified time offset.")
def shift(
    target: Path = typer.Argument(
        Path("."),
        help="Path to the video file or directory containing video files.",
        exists=True,
        readable=True,
        resolve_path=True,
    ),
    ms_offset: int = typer.Argument(
        help="Time offset in milliseconds to shift the subtitles."
    ),
    quiet: bool = QuietOption,
    recursive: bool = RecursiveOption,
):
    """Display information about the specified video file or all video files in the given directory."""
    console = Console(quiet=quiet)
    wrapper = SubWrapper(console)
    files = collect_subtitles_files(target, recursive)

    if not files:
        console.print(f"[yellow]No subtitles files found in {target}[/yellow]")
        raise typer.Exit(0)

    subs = wrapper.load_subtitles(files)
    for sub in subs:
        sub.shift(ms=ms_offset)
        console.print(f"[green]Shifted {sub.path.name} by {ms_offset} ms[/green]")

    codes = wrapper.save_subtitles(subs)
    success_count = sum(1 for code in codes if code == 0)
    error_count = len(codes) - success_count
    color = "green" if error_count == 0 else "yellow" if success_count > 0 else "red"
    console.print(
        f"[{color}]Processing complete:[/] {success_count} succeeded, {error_count} failed."
    )
    if not success_count:
        raise typer.Exit(code=1)
