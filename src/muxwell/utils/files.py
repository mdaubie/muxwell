from pathlib import Path

VIDEO_EXTENSIONS = [".mkv", ".mp4", ".m4v", ".avi", ".mov", ".wmv", ".flv"]


def collect_files(dir: Path, extensions: list[str]) -> list[Path]:
    """Collect all files with the given extensions in the specified directory."""
    files: list[Path] = []
    for ext in extensions:
        files.extend(dir.glob(f"*{ext}"))
    return files


def collect_video_files(dir: Path) -> list[Path]:
    """Collect all video files in the specified directory."""
    return collect_files(dir, VIDEO_EXTENSIONS)
