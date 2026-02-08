from __future__ import annotations

from pathlib import Path

from .filenames import Episode, Movie, MultiEpisode, parse_filename


def infer_title(path: Path) -> str | None:
    """Infer title from filename."""
    if item := parse_filename(path.name):
        return format_title(item)


def format_title(item: Movie | Episode | MultiEpisode) -> str:
    if isinstance(item, (Movie)):
        return f"{item.title} ({item.year})" if item.year else item.title
    elif isinstance(item, (Episode)):
        return f"{item.title} S{item.season:02d}E{item.episode:02d}"
    else:
        episode_str = ",".join(f"{e:02d}" for e in item.episodes)
        return f"{item.title} S{item.season:02d}E{episode_str}"
