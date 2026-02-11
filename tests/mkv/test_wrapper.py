"""Tests for muxwell.mkv.wrapper module."""

from __future__ import annotations

from pathlib import Path

import pytest
from rich.console import Console

from muxwell.mkv.wrapper import MKVWrapper

from .conftest import MKVFileBuilder


class TestMKVWrapper:
    """Tests for the MKVWrapper class."""

    @pytest.fixture
    def wrapper(self, console: Console) -> MKVWrapper:
        """Create an MKVWrapper instance for testing."""
        return MKVWrapper(console)

    @pytest.mark.parametrize(
        ["video_files"],
        [
            pytest.param(["existent", "existent"], id="multiple"),
            pytest.param(["nested"], id="single_nested"),
        ],
        indirect=["video_files"],
    )
    def test_load_videos(self, wrapper: MKVWrapper, video_files: list[Path]):
        """Test loading multiple videos."""
        videos = wrapper.load_videos(video_files)

        assert len(videos) == len(video_files)
        for video, path in zip(videos, video_files, strict=True):
            assert video.file_path == path

    @pytest.mark.parametrize(
        ["video_files"],
        [
            pytest.param(["unexistent"], id="single_unexistent"),
            pytest.param(["existent", "unexistent"], id="mixed_existent_unexistent"),
        ],
        indirect=["video_files"],
    )
    def test_load_videos_raises_file_not_found(
        self, wrapper: MKVWrapper, video_files: list[Path]
    ):
        """Test loading a non-existent video file."""
        with pytest.raises(FileNotFoundError):
            wrapper.load_videos(video_files)

    @pytest.mark.parametrize(
        ["video_files", "mkv_file_builders", "expected_result"],
        [
            pytest.param(
                ["existent", "existent"],
                ["success", "success"],
                [0, 0],
                id="multiple_mux_success",
            ),
            pytest.param(
                ["nested_existent"],
                ["error"],
                [1],
                id="single_nested_mux_fails",
            ),
            pytest.param(
                ["existent", "existent"],
                ["success", "error"],
                [0, 1],
                id="multiple_mux_partial_failure",
            ),
            pytest.param(
                [],
                [],
                [],
                id="empty_list",
            ),
        ],
        indirect=["video_files", "mkv_file_builders"],
    )
    def test_mux_videos(
        self,
        wrapper: MKVWrapper,
        video_files: list[Path],
        mkv_file_builders: list[MKVFileBuilder],
        expected_result: list[int],
    ):
        """Test muxing multiple videos with various file existence scenarios."""
        # This test will be implemented in the next step
        videos = [
            (path.with_suffix(".tmp"), mkv_file_builder(path))
            for path, mkv_file_builder in zip(
                video_files, mkv_file_builders, strict=True
            )
        ]

        result = wrapper.mux_videos(videos)
        assert result == expected_result
        for output_path, video in videos:
            video.mux.assert_called_once()
            # Success: output renamed to input, Error: output cleaned up
            assert not output_path.exists()
            # Success: input now has muxed content, Error: input unchanged
            assert video.file_path.exists()
