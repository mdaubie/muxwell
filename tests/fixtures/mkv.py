# pyright: reportPrivateUsage=false
from __future__ import annotations

from collections.abc import Callable
from pathlib import Path
from typing import Protocol
from unittest.mock import MagicMock

import pytest
from pymkv import MKVTrack
from pytest import FixtureRequest

from muxwell.mkv import MKVFile


class MKVFileBuilder(Protocol):
    def __call__(
        self,
        filepath: Path,
        tracks: list[MKVTrack] | None = None,
    ) -> MKVFile: ...


MuxMock = Callable[[Path, Callable[[int], None]], int]


def _mux_success(output_path: Path, progress_handler: Callable[[int], None]) -> int:
    """Simulate successful muxing by creating output file and reporting progress."""
    output_path.touch()
    for i in range(0, 101, 20):
        progress_handler(i)
    return 0


def _mux_error(output_path: Path, progress_handler: Callable[[int], None]) -> int:
    """Simulate a muxing error."""
    raise ValueError("Simulated muxing error")


def _create_mkv_builder(mux_mock: MuxMock) -> MKVFileBuilder:
    """Create a builder function that constructs mocked MKVFile instances."""

    def _builder(filepath: Path, tracks: list[MKVTrack] | None = None) -> MKVFile:
        real_mkv = MKVFile(filepath)
        if tracks is not None:
            real_mkv.tracks.extend(tracks)
            real_mkv._number_file = len(real_mkv.tracks)
            real_mkv._snapshot = real_mkv.info
        real_mkv.mux = MagicMock(side_effect=mux_mock)
        return real_mkv

    return _builder


@pytest.fixture
def mkv_file_builder_success() -> MKVFileBuilder:
    """Provide a mocked MKVFile builder with successful mux behavior."""
    return _create_mkv_builder(_mux_success)


@pytest.fixture
def mkv_file_builder_error() -> MKVFileBuilder:
    """Provide a mocked MKVFile builder with failing mux behavior."""
    return _create_mkv_builder(_mux_error)


@pytest.fixture
def mkv_file_builder(
    request: FixtureRequest,
    mkv_file_builder_success: MKVFileBuilder,
    mkv_file_builder_error: MKVFileBuilder,
) -> MKVFileBuilder:
    """Select mkv builder fixture, defaulting to success."""
    param = getattr(request, "param", "success")
    return mkv_file_builder_error if param == "error" else mkv_file_builder_success


@pytest.fixture
def mkv_file_builders(
    request: FixtureRequest,
    mkv_file_builder_success: MKVFileBuilder,
    mkv_file_builder_error: MKVFileBuilder,
) -> list[MKVFileBuilder]:
    """Provide a list of MKVFileBuilder instances based on test parameters."""
    builders: list[MKVFileBuilder] = []
    for param in request.param:
        match param:
            case "success":
                builders.append(mkv_file_builder_success)
            case "error":
                builders.append(mkv_file_builder_error)
            case _:
                raise ValueError(f"Invalid mkv_file_builder parameter: {param}")
    return builders


@pytest.fixture(autouse=True)
def patch_mkv_file(monkeypatch: pytest.MonkeyPatch) -> None:
    """Patch MKVFile initialization and muxing globally for unit tests."""

    def _patched_init(self: MKVFile, file_path: str | Path) -> None:
        file_path = Path(file_path)
        if not file_path.is_file():
            raise FileNotFoundError(f'"{file_path}" does not exist')
        self.file_path = file_path
        self.title = None

        video_track = MKVTrack(file_path.as_posix())
        self.tracks = [video_track]
        self._number_file = len(self.tracks)
        self._snapshot = self.info

    def _patched_mux(
        self: MKVFile,
        output_path: Path,
        progress_handler: Callable[[int], None],
    ) -> int:
        return _mux_success(output_path, progress_handler)

    monkeypatch.setattr("muxwell.mkv.models.MKVFile.__init__", _patched_init)
    monkeypatch.setattr("muxwell.mkv.models.MKVFile.mux", _patched_mux)


@pytest.fixture(autouse=True)
def patch_mkv_track(monkeypatch: pytest.MonkeyPatch):
    """Patch MKVTrack initialization and muxing globally for unit tests."""

    def _patched_init(self: MKVTrack, file_path: str) -> None:
        if not Path(file_path).is_file():
            raise FileNotFoundError(f'"{file_path}" does not exist')
        self._file_path = file_path
        self._track_codec = None
        self._track_type = "subtitles"
        self._track_id = 0
        self.track_name = None
        self._language = None
        self.default_track = False
        self.forced_track = False

    monkeypatch.setattr("tests.fixtures.mkv.MKVTrack.__init__", _patched_init)


@pytest.fixture
def mkv_file(video_file: Path) -> MKVFile:
    return MKVFile(video_file)


@pytest.fixture
def mkv_file_with_subs(
    video_file: Path,
    subs_file: Path,
    mkv_file_builder: MKVFileBuilder,
) -> MKVFile:
    return mkv_file_builder(video_file, tracks=[MKVTrack(subs_file.as_posix())])
