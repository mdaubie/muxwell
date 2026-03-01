from __future__ import annotations

from functools import lru_cache
from pathlib import Path

import chardet

VIDEO_EXTENSIONS = [".mkv", ".mp4", ".m4v", ".avi", ".mov", ".wmv", ".flv"]
SUBTITLES_EXTENSIONS = [".srt", ".ass", ".ssa"]


def collect_files(target: Path, extensions: list[str], recursive: bool) -> list[Path]:
    """Collect all files with the given extensions in the specified directory."""
    if target.is_file():
        if any(target.suffix.lower() == ext for ext in extensions):
            return [target]
        else:
            raise ValueError(
                f"The file {target} does not have a supported video extension."
            )

    files: list[Path] = []
    for ext in extensions:
        if recursive:
            files.extend(target.rglob(f"*{ext}"))
        else:
            files.extend(target.glob(f"*{ext}"))
    return files


def collect_video_files(target: Path, recursive: bool) -> list[Path]:
    """Collect all video files in the specified directory."""
    return collect_files(target, VIDEO_EXTENSIONS, recursive)


def collect_subtitles_files(target: Path, recursive: bool) -> list[Path]:
    """Collect all subtitles files in the specified directory."""
    return collect_files(target, SUBTITLES_EXTENSIONS, recursive)


@lru_cache
def _read_file_bytes(path: Path) -> bytes:
    return path.read_bytes()


@lru_cache
def _detect_file(path: Path):
    return chardet.detect(_read_file_bytes(path))


def get_encoding(sub_path: Path) -> str | None:
    data = _read_file_bytes(sub_path)
    for encoding in ("utf-8-sig", "utf-8"):
        try:
            data.decode(encoding)
            return encoding
        except UnicodeDecodeError:
            pass
    return _detect_file(sub_path).get("encoding")
