from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from functools import lru_cache
from pathlib import Path

from rich.console import Console
from rich.markup import escape
from rich.progress import Progress, SpinnerColumn, TextColumn

from .models import SubFile


class SubWrapper:
    def __init__(self, console: Console):
        self.console = console

    def load_subtitles(self, file_paths: list[Path]) -> list[SubFile]:
        """Load multiple subtitle files concurrently with caching. Returns a list of SubFile objects."""
        with (
            Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=self.console,
            ) as progress,
            ThreadPoolExecutor() as executor,
        ):

            def load_subtitle(file_path: Path) -> SubFile:
                progress.add_task(f"Loading {escape(file_path.name)}...", total=None)
                return _load_subtitle(file_path)

            return list(executor.map(load_subtitle, file_paths))

    def save_subtitles(self, subtitles: list[SubFile]) -> list[int]:
        """Save multiple subtitle files concurrently with caching. Returns a list of status codes (0 for success, 1 for failure)."""
        with (
            Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=self.console,
            ) as progress,
            ThreadPoolExecutor() as executor,
        ):

            def save_subtitle(sub: SubFile) -> int:
                progress.add_task(f"Saving {escape(sub.path.name)}...", total=None)
                output_path = sub.path.with_suffix(suffix=sub.path.suffix + ".tmp")
                try:

                    sub.save(output_path.as_posix(), format_=sub.format)
                    sub.path.unlink()
                    output_path.rename(sub.path)
                    return 0
                except Exception as e:
                    self.console.print(
                        f"[red]Error saving {escape(sub.path.name)}: {escape(str(e))}[/red]"
                    )
                    output_path.unlink(missing_ok=True)
                    return 1

            return list(executor.map(save_subtitle, subtitles))


@lru_cache(maxsize=32)
def _load_subtitle(file_path: Path) -> SubFile:
    return SubFile(file_path)
