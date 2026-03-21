from __future__ import annotations

from collections.abc import Callable
from pathlib import Path
from unittest.mock import MagicMock

import pytest
from pytest import FixtureRequest

from muxwell.mkv import MKVFile

MKVFileBuilder = Callable[[Path], MagicMock]
MuxMock = Callable[[Path, Callable[[int], None]], int]


def _mock_init_mkv(
    mkv: MKVFile,
    filepath: Path,
) -> None:
    """Initialize minimal MKVFile state needed by unit tests."""
    if not filepath.is_file():
        raise FileNotFoundError(f'"{filepath}" does not exist')
    mkv.file_path = filepath


def _create_mkv_builder(mux_mock: MuxMock) -> MKVFileBuilder:
    """Create a builder function that constructs mocked MKVFile instances."""

    def _builder(filepath: Path) -> MagicMock:
        real_mkv = object.__new__(MKVFile)
        _mock_init_mkv(real_mkv, filepath)
        real_mkv.mux = MagicMock(side_effect=mux_mock)
        wrapped = MagicMock(spec=MKVFile, wraps=real_mkv)
        wrapped.file_path = real_mkv.file_path
        return wrapped

    return _builder


@pytest.fixture
def mkv_file_builder_success() -> MKVFileBuilder:
    """Provide a mocked MKVFile builder with successful mux behavior."""

    def mux_mock(output_path: Path, progress_handler: Callable[[int], None]) -> int:
        """Simulates successful muxing by creating output file and reporting progress."""
        output_path.touch()
        for i in range(0, 101, 20):
            progress_handler(i)
        return 0

    return _create_mkv_builder(mux_mock)


@pytest.fixture
def mkv_file_builder_error() -> MKVFileBuilder:
    """Provide a mocked MKVFile builder with failing mux behavior."""

    def mux_mock(output_path: Path, progress_handler: Callable[[int], None]) -> int:
        """Simulates muxing error by raising an exception."""
        raise ValueError("Simulated muxing error")

    return _create_mkv_builder(mux_mock)


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
def patch_mkv_file(
    monkeypatch: pytest.MonkeyPatch, mkv_file_builder: MKVFileBuilder
) -> None:
    """Patch MKVFile globally for unit tests."""
    monkeypatch.setattr("muxwell.mkv.wrapper.MKVFile", mkv_file_builder)
