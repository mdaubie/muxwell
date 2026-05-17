from __future__ import annotations

from pathlib import Path
from unittest.mock import Mock

from pytest import MonkeyPatch

import muxwell.engine as engine_module
from muxwell.engine import (
    FilePlan,
    ProcessingEngine,
    _diff_mkv,  # pyright: ignore[reportPrivateUsage]
)
from muxwell.mkv.models import MkvInfo, TrackInfo


def _track(
    track_id: int,
    filepath: str,
    *,
    lang: str | None = "eng",
    track_type: str | None = "subtitles",
    codec: str | None = "SubRip/SRT",
    name: str | None = None,
    default: bool = False,
    forced: bool = False,
) -> TrackInfo:
    return TrackInfo(
        id=track_id,
        type=track_type,
        codec=codec,
        lang=lang,
        name=name,
        default=default,
        forced=forced,
        filepath=filepath,
    )


def test_diff_mkv_handles_duplicate_track_ids_without_collisions():
    before = MkvInfo(
        path=Path("video.mkv"),
        title=None,
        tracks=[
            _track(0, "video.mkv", track_type="video", codec="H.264"),
            _track(0, "video.mkv", track_type="audio", codec="AAC", lang="jpn"),
        ],
    )
    after = MkvInfo(
        path=Path("video.mkv"),
        title=None,
        tracks=[
            _track(0, "video.mkv", track_type="video", codec="H.264"),
            _track(0, "subtitle.srt", lang=None),
        ],
    )

    lines = _diff_mkv(before, after)

    assert len(lines) == 2
    assert lines[0].startswith("- Track 1")
    assert "audio" in lines[0]
    assert lines[1].startswith("+ Track 1")
    assert "subtitle.srt" in lines[1]
    assert "lang=und" in lines[1]


def test_diff_mkv_language_change_labels_undefined_explicitly():
    before = MkvInfo(
        path=Path("video.mkv"),
        title=None,
        tracks=[_track(2, "video.mkv", lang=None)],
    )
    after = MkvInfo(
        path=Path("video.mkv"),
        title=None,
        tracks=[_track(2, "video.mkv", lang="eng")],
    )

    lines = _diff_mkv(before, after)

    assert lines == ["~ Track 0: language und -> eng"]


def test_print_plan_handles_diff_lines(
    monkeypatch: MonkeyPatch, console_mock: Mock
) -> None:
    """Print plan lines with expected styles for each diff prefix."""
    # Mock data
    before = MkvInfo(
        path=Path("video.mkv"),
        title=None,
        tracks=[
            TrackInfo(
                id=0,
                type="video",
                codec="H.264",
                lang=None,
                name=None,
                default=False,
                forced=False,
                filepath="video.mkv",
            )
        ],
    )
    after = MkvInfo(
        path=Path("video.mkv"),
        title=None,
        tracks=[
            TrackInfo(
                id=0,
                type="video",
                codec="H.264",
                lang="eng",
                name=None,
                default=False,
                forced=False,
                filepath="video.mkv",
            )
        ],
    )

    plan = FilePlan(
        video=Mock(snapshot=before, info=after), output_path=Path("output.mkv")
    )
    engine = ProcessingEngine(console_mock)

    def _fake_diff_mkv(_before: MkvInfo, _after: MkvInfo) -> list[str]:
        return [
            "+ added",
            "- removed",
            "~ Track 0: language und -> eng",
            "unchanged",
        ]

    monkeypatch.setattr(engine_module, "_diff_mkv", _fake_diff_mkv)

    engine.print_plan([plan])

    console_mock.print.assert_any_call(
        "[bold]Dry run:[/] the following changes would be applied"
    )
    console_mock.print.assert_any_call("[green]+ added[/]")
    console_mock.print.assert_any_call("[red]- removed[/]")
    console_mock.print.assert_any_call("[yellow]~ Track 0: language und -> eng[/]")
    console_mock.print.assert_any_call("[white]unchanged[/]")
