from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

import typer
from rich.console import Console

from .actions import Action, ActionContext
from .mkv import MKVFile, MKVWrapper
from .operations import Operation


@dataclass
class FilePlan:
    video: MKVFile
    output_path: Path


class ProcessingEngine:
    def __init__(self, console: Console):
        self.console = console
        self.mkv_wrapper = MKVWrapper(console)

    def _collect_operations(
        self, target: Path, actions: list[Action], recursive: bool
    ) -> dict[Path, list[Operation]]:
        context = ActionContext(target, self.console, recursive)
        reduced = defaultdict[Path, list[Operation]](list)

        for action in actions:
            for file_path, operations in action.analyze(context).items():
                reduced[file_path].extend(operations)
        return reduced

    def plan(
        self, target: Path, actions: list[Action], recursive: bool
    ) -> list[FilePlan]:
        """Process the target with the given actions."""
        operations_map = self._collect_operations(target, actions, recursive)
        mkv_files = self.mkv_wrapper.load_videos(list(operations_map.keys()))

        for mkv_file in mkv_files:
            for operation in operations_map[mkv_file.file_path]:
                operation.apply(mkv_file)
        return [
            FilePlan(
                video=video, output_path=self._compute_output_path(video.file_path)
            )
            for video in mkv_files
            if video.changed
        ]

    def _compute_output_path(self, source: Path) -> Path:
        return source.with_suffix(source.suffix + ".tmp")

    def execute(self, plans: list[FilePlan]):
        """Execute the given plans."""
        codes = self.mkv_wrapper.mux_videos(
            [(plan.output_path, plan.video) for plan in plans]
        )
        success_count = sum(1 for code in codes if code == 0)
        error_count = len(codes) - success_count
        color = (
            "green" if error_count == 0 else "yellow" if success_count > 0 else "red"
        )
        self.console.print(
            f"[{color}]Processing complete:[/] {success_count} succeeded, {error_count} failed."
        )
        if not success_count:
            raise typer.Exit(code=1)
