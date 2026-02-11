from __future__ import annotations

from collections.abc import Callable
from pathlib import Path
from unittest.mock import MagicMock

import pytest
from pytest import FixtureRequest, MonkeyPatch

from muxwell.mkv import MKVFile

MKVFileBuilder = Callable[[Path], MagicMock]
MuxMock = Callable[[Path, Callable[[int], None]], int]


def _create_mkv_builder(mux_mock: MuxMock) -> MKVFileBuilder:
    """Create a builder function that constructs mocked MKVFile instances"""

    def _builder(filepath: Path) -> MagicMock:
        if not filepath.is_file():
            raise FileNotFoundError(f'"{filepath}" does not exist')
        mock = MagicMock(spec=MKVFile)
        mock.file_path = filepath
        mock.mux.side_effect = mux_mock
        return mock

    return _builder


@pytest.fixture
def mkv_file_builder_success() -> MKVFileBuilder:
    """Fixture that provides a mocked MKVFile instance with default behavior"""

    def mux_mock(output_path: Path, progress_handler: Callable[[int], None]) -> int:
        """Simulates successful muxing by creating output file and reporting progress."""
        print(f"Default mux side effect called with output_path={output_path}")
        output_path.touch()  # Simulate creating the output file
        for i in range(0, 101, 20):
            progress_handler(i)
        return 0

    return _create_mkv_builder(mux_mock)


@pytest.fixture
def mkv_file_builder_error() -> MKVFileBuilder:
    """Fixture that provides a mocked MKVFile instance that simulates an error during muxing"""

    def mux_mock(output_path: Path, progress_handler: Callable[[int], None]) -> int:
        """Simulates muxing error by raising an exception."""
        print(f"Error mux side effect called with output_path={output_path}")
        raise ValueError("Simulated muxing error")

    return _create_mkv_builder(mux_mock)


@pytest.fixture
def mkv_file_builder(
    request: FixtureRequest,
    mkv_file_builder_success: MKVFileBuilder,
    mkv_file_builder_error: MKVFileBuilder,
) -> MKVFileBuilder:
    """Fixture that can be used with indirect parametrization.

    Use with @pytest.mark.parametrize("mkv_file_builder", ["success", "error"], indirect=True)
    """
    param = getattr(request, "param", "success")
    return mkv_file_builder_error if param == "error" else mkv_file_builder_success


@pytest.fixture
def mkv_file_builders(
    request: FixtureRequest,
    mkv_file_builder_success: MKVFileBuilder,
    mkv_file_builder_error: MKVFileBuilder,
) -> list[MKVFileBuilder]:
    """Fixture that provides a list of MKVFileBuilder instances based on the test parameter."""
    builders: list[MKVFileBuilder] = []
    for p in request.param:
        match p:
            case "success":
                builders.append(mkv_file_builder_success)
            case "error":
                builders.append(mkv_file_builder_error)
            case _:
                raise ValueError(f"Invalid mkv_file_builder parameter: {p}")
    return builders


@pytest.fixture(autouse=True)
def patch_mkv_file(monkeypatch: MonkeyPatch, mkv_file_builder: MKVFileBuilder) -> None:
    """Automatically patch MKVFile for all tests in this module.

    This fixture provides default mock behavior for MKVFile. Tests can override
    this by using indirect parametrization with 'mkv_file_builder'.
    For tests needing multiple different builders, use 'mkv_file_builders' fixture
    and handle patching manually within the test.
    """
    monkeypatch.setattr("muxwell.mkv.wrapper.MKVFile", mkv_file_builder)
