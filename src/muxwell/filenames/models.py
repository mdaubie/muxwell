from __future__ import annotations

from abc import ABC
from dataclasses import dataclass


@dataclass
class ParsedFilename(ABC):
    title: str

    def matches(self, other: ParsedFilename) -> bool:
        """Determine if this parsed filename matches another based on title and any additional attributes."""
        if self.title.lower() != other.title.lower():
            return False
        # Compare all other attributes (e.g., year, season/episode) if they exist
        for attr in set(vars(self).keys()) | set(vars(other).keys()):
            if attr == "title":
                continue
            if getattr(self, attr, None) != getattr(other, attr, None):
                return False
        return True


@dataclass
class Movie(ParsedFilename):
    year: int | None


@dataclass
class Episode(ParsedFilename):
    season: int
    episode: int


@dataclass
class MultiEpisode(ParsedFilename):
    season: int
    episodes: list[int]
