from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

from ..mkv import MkvInfo, MKVWrapper
from ..utils.files import collect_video_files
from .common import QuietOption, RecursiveOption


def info(
    target: Path = typer.Argument(
        Path("."),
        help="Path to the video file or directory containing video files.",
        exists=True,
        readable=True,
        resolve_path=True,
    ),
    quiet: bool = QuietOption,
    recursive: bool = RecursiveOption,
):
    """Display information about the specified video file or all video files in the given directory."""
    console = Console(quiet=quiet)
    files = collect_video_files(target, recursive)

    if not files:
        console.print(f"[yellow]No video files found in {target}[/yellow]")
        raise typer.Exit(0)

    wrapper = MKVWrapper(console)
    videos = wrapper.load_videos(files)

    _print_table([video.info for video in videos])


def _print_table(videos: list[MkvInfo]):
    console = Console()
    table = Table("File", "Title", "Tracks")
    for video in videos:
        tt = Table("ID", "Type", "Codec", "Lang", "Name", "Default", "Forced")
        for track in video.tracks:
            tt.add_row(
                str(track.id),
                track.type or "-",
                track.codec or "-",
                track.lang or "-",
                track.name or "-",
                "Yes" if track.default else "No",
                "Yes" if track.forced else "No",
            )
        table.add_row(video.path.name, video.title or "-", tt)
    console.print(table)
