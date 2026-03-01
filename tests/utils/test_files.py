"""Tests for muxwell.utils.files module."""

from __future__ import annotations

from pathlib import Path

from muxwell.utils.files import collect_subtitles_files, collect_video_files


class TestCollectVideoFiles:
    """Tests for the collect_video_files function."""

    def test_collect_video_files_single_file(self, video_file: Path):
        """Test collecting a single video file."""
        files = collect_video_files(video_file, recursive=False)

        assert len(files) == 1
        assert files[0] == video_file

    def test_collect_video_files_directory(
        self, video_files: list[Path], subs_file: Path
    ):
        """Test collecting video files from directory."""
        tmp_path = video_files[0].parent

        files = collect_video_files(tmp_path, recursive=False)

        assert len(files) == len(video_files)
        for f in files:
            assert f in video_files
            assert f != subs_file

    def test_collect_video_files_recursive(self, tmp_path: Path):
        """Test collecting video files recursively."""
        (tmp_path / "test1.mkv").touch()

        subdir = tmp_path / "subdir"
        subdir.mkdir()
        (subdir / "test2.mp4").touch()

        files = collect_video_files(tmp_path, recursive=True)

        assert len(files) == 2


class TestCollectSubtitlesFiles:
    """Tests for the collect_subtitles_files function."""

    def test_collect_subtitles_single_file(self, srt_file: Path):
        """Test collecting a single subtitle file."""
        files = collect_subtitles_files(srt_file, recursive=False)

        assert len(files) == 1
        assert files[0] == srt_file

    def test_collect_subtitles_directory(
        self, tmp_path: Path, subs_files: list[Path], video_file: Path
    ):
        """Test collecting subtitle files from directory."""
        files = collect_subtitles_files(tmp_path, recursive=False)

        assert len(files) == len(subs_files)
        for f in files:
            assert f in subs_files
            assert f != video_file

    def test_collect_subtitles_recursive(self, tmp_path: Path):
        """Test collecting subtitle files recursively."""
        (tmp_path / "test1.srt").touch()

        subdir = tmp_path / "subdir"
        subdir.mkdir()
        (subdir / "test2.ass").touch()

        nested = subdir / "nested"
        nested.mkdir()
        (nested / "test3.ssa").touch()

        files = collect_subtitles_files(tmp_path, recursive=True)

        assert len(files) == 3

    def test_collect_subtitles_non_recursive(self, tmp_path: Path):
        """Test collecting subtitle files non-recursively."""
        (tmp_path / "test1.srt").touch()

        subdir = tmp_path / "subdir"
        subdir.mkdir()
        (subdir / "test2.ass").touch()

        files = collect_subtitles_files(tmp_path, recursive=False)

        assert len(files) == 1
        assert files[0].name == "test1.srt"
