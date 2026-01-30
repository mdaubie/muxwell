from concurrent.futures import ThreadPoolExecutor
from functools import lru_cache
from pathlib import Path

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from .models import MKVFile

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
                progress.add_task(f"Loading {file_path.name}...", total=None)
                return _load_mkv(file_path)

            return list(executor.map(load_video, file_paths))


@lru_cache(maxsize=32)
def _load_mkv(file_path: Path) -> MKVFile:
    return MKVFile(file_path)
