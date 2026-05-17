from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

import typer
from rich.console import Console
from rich.markup import escape

from .actions import Action, ActionContext
from .mkv import MKVFile, MkvInfo, MKVWrapper, TrackInfo
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
            for operation in sorted(operations_map[mkv_file.file_path]):
                operation.apply(mkv_file)
        return [
            FilePlan(
                video=video, output_path=self._compute_output_path(video.file_path)
            )
            for video in mkv_files
            if video.changed
        ]

    def print_plan(self, plans: list[FilePlan]):
        """Print a dry-run summary for the given plans."""
        self.console.print("[bold]Dry run:[/] the following changes would be applied")
        for plan in plans:
            before = plan.video.snapshot
            after = plan.video.info
            self.console.print(
                f"\n[bold]{escape(str(plan.video.file_path))}[/] -> "
                f"{escape(str(plan.output_path))}"
            )
            for line in _diff_mkv(before, after):
                if line.startswith("+"):
                    style = "green"
                elif line.startswith("-"):
                    style = "red"
                elif line.startswith("~"):
                    style = "yellow"
                else:
                    style = "white"
                self.console.print(f"[{style}]{escape(line)}[/]")

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


def _track_key(track: TrackInfo) -> tuple[int, str]:
    return (track.id, track.filepath)


def _format_track(
    track: TrackInfo, display_index: int, *, include_path: bool = False
) -> str:
    track_type = track.type or "unknown"
    codec = track.codec or "unknown"
    language = track.lang or "und"
    name = f", name={track.name}" if track.name else ""
    path = f", {track.filepath}" if include_path else ""
    return (
        f"Track {display_index} ({track_type}, {codec}, lang={language}, "
        f"default={track.default}, forced={track.forced}{name}{path})"
    )


def _diff_track(before: TrackInfo, after: TrackInfo) -> list[str]:
    changes: list[str] = []
    for label, before_value, after_value in (
        ("type", before.type, after.type),
        ("codec", before.codec, after.codec),
        ("language", before.lang or "und", after.lang or "und"),
        ("name", before.name, after.name),
        ("default", before.default, after.default),
        ("forced", before.forced, after.forced),
    ):
        if before_value != after_value:
            changes.append(f"{label} {before_value} -> {after_value}")
    return changes


def _diff_mkv(before: MkvInfo, after: MkvInfo) -> list[str]:
    lines: list[str] = []
    modified_lines: list[str] = []
    removed_lines: list[str] = []
    added_lines: list[str] = []

    if before.title != after.title:
        lines.append(f"~ Title: {before.title!r} -> {after.title!r}")

    before_groups = defaultdict[tuple[int, str], list[TrackInfo]](list)
    after_groups = defaultdict[tuple[int, str], list[TrackInfo]](list)
    before_track_index = {id(track): idx for idx, track in enumerate(before.tracks)}
    after_track_index = {id(track): idx for idx, track in enumerate(after.tracks)}
    for track in before.tracks:
        before_groups[_track_key(track)].append(track)
    for track in after.tracks:
        after_groups[_track_key(track)].append(track)

    for key in sorted(set(before_groups) | set(after_groups)):
        before_tracks = before_groups.get(key, [])
        after_tracks = after_groups.get(key, [])
        shared_count = min(len(before_tracks), len(after_tracks))

        for index in range(shared_count):
            changes = _diff_track(before_tracks[index], after_tracks[index])
            if changes:
                modified_lines.append(
                    f"~ Track {after_track_index[id(after_tracks[index])]}: "
                    + ", ".join(changes)
                )

        for track in before_tracks[shared_count:]:
            removed_lines.append(
                f"- {_format_track(track, before_track_index[id(track)])}"
            )

        for track in after_tracks[shared_count:]:
            added_lines.append(
                f"+ {_format_track(track, after_track_index[id(track)], include_path=True)}"
            )

    lines.extend(modified_lines)
    lines.extend(removed_lines)
    lines.extend(added_lines)

    return lines
