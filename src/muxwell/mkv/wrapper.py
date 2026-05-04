from __future__ import annotations

import os
from collections.abc import Sequence
from concurrent.futures import ThreadPoolExecutor
from functools import lru_cache
from pathlib import Path

from rich.console import Console
from rich.markup import escape
from rich.progress import Progress, SpinnerColumn, TextColumn

from .models import MKVFile

os.environ["LANG"] = "en_US.UTF-8"  # Ensure consistent language for mkvtoolnix output
console = Console()


class MKVWrapper:
    def __init__(self, console: Console):
        self.console = console

    def load_videos(self, file_paths: list[Path]) -> list[MKVFile]:
        """Load multiple MKV files concurrently with caching and progress indication."""
        with (
            Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=self.console,
            ) as progress,
            ThreadPoolExecutor() as executor,
        ):

            def load_video(file_path: Path) -> MKVFile:
                progress.add_task(f"Loading {escape(file_path.name)}...", total=None)
                return _load_mkv(file_path)

            return list(executor.map(load_video, file_paths))

    def mux_videos(self, videos: Sequence[tuple[Path, MKVFile]]) -> list[int]:
        """Mux multiple MKV files concurrently with progress indication."""
        with (
            Progress(console=self.console) as progress,
            ThreadPoolExecutor() as executor,
        ):

            def mux_video(arg: tuple[Path, MKVFile]) -> int:
                path, video = arg
                id = progress.add_task(f"Muxing {escape(path.name)}...", total=100)

                def progress_handler(progress_value: int):
                    progress.update(id, completed=progress_value)

                try:
                    video.mux(  # pyright: ignore[reportUnknownMemberType]
                        output_path=path,
                        progress_handler=progress_handler,
                    )
                    video.file_path.unlink()
                    path.rename(video.file_path)
                    return 0
                except ValueError as e:
                    self.console.print(
                        f"[red]Error muxing {escape(path.name)}: {escape(str(e))}[/red]"
                    )
                    path.unlink(missing_ok=True)
                    return 1

            return list(executor.map(mux_video, videos))


@lru_cache(maxsize=32)
def _load_mkv(file_path: Path) -> MKVFile:
    return MKVFile(file_path)
