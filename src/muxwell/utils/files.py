from pathlib import Path

VIDEO_EXTENSIONS = [".mkv", ".mp4", ".m4v", ".avi", ".mov", ".wmv", ".flv"]


def collect_files(target: Path, extensions: list[str]) -> list[Path]:
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
        files.extend(target.glob(f"*{ext}"))
    return files


def collect_video_files(target: Path) -> list[Path]:
    """Collect all video files in the specified directory."""
    return collect_files(target, VIDEO_EXTENSIONS)
