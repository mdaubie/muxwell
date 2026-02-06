from __future__ import annotations

from abc import ABC
from dataclasses import dataclass


@dataclass
class ParsedFilename(ABC):
    title: str


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
