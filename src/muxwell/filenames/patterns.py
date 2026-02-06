from __future__ import annotations

import re
from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from .models import Episode, Movie, MultiEpisode, ParsedFilename

T = TypeVar("T", bound=ParsedFilename)


class Parser(Generic[T], ABC):
    """Abstract parser returning specific ParsedFilename type."""

    @abstractmethod
    def parse(self, cleaned_name: str) -> T | None:
        pass


class MovieYearParser(Parser[Movie]):
    """Matches patterns like '.2010.' or '(2010)'"""

    def parse(self, cleaned_name: str) -> Movie | None:
        # Match 4-digit year (1900-2099)
        pattern = r"\b(19\d{2}|20\d{2})\b"
        matches = list(re.finditer(pattern, cleaned_name))

        if not matches:
            return None

        # Use the last year found (handles cases like "Sonic.the.Hedgehog.2020.2020")
        match = matches[-1]
        year = int(match.group(1))

        # Title is everything before the last year
        title = cleaned_name[: match.start()].strip()

        # If no title before the year, it might be a year-titled movie like "1917"
        # In that case, check if there's another year before this one
        if not title and len(matches) > 1:
            # The title is the previous year
            prev_match = matches[-2]
            title = prev_match.group(1)
            year = int(match.group(1))
        elif not title:
            return None

        return Movie(title, year)


class SeasonEpisodeCompactParser(Parser[Episode]):
    """Matches S01E01 pattern"""

    def parse(self, cleaned_name: str) -> Episode | None:
        # Match S##E## pattern (case insensitive)
        pattern = r"\bs(\d{1,2})e(\d{1,2})\b"
        match = re.search(pattern, cleaned_name, re.IGNORECASE)

        if not match:
            return None

        season = int(match.group(1))
        episode = int(match.group(2))

        # Title is everything before the season/episode marker
        title = cleaned_name[: match.start()].strip()

        return Episode(title, season, episode)


class SeasonEpisodeXParser(Parser[Episode]):
    """Matches 01x01 pattern"""

    target_type = Episode

    def parse(self, cleaned_name: str) -> Episode | None:
        # Match ##x## pattern (case insensitive)
        pattern = r"\b(\d{1,2})x(\d{1,2})\b"
        match = re.search(pattern, cleaned_name, re.IGNORECASE)

        if not match:
            return None

        season = int(match.group(1))
        episode = int(match.group(2))

        # Title is everything before the season/episode marker
        title = cleaned_name[: match.start()].strip()

        return Episode(title, season, episode)


class EpisodeOnlyParser(Parser[Episode]):
    """Matches Episode.01 pattern"""

    def parse(self, cleaned_name: str) -> Episode | None:
        # Match Episode.## pattern (case insensitive)
        pattern = r"\bEpisode[\. ](\d{1,2})\b"
        match = re.search(pattern, cleaned_name, re.IGNORECASE)

        if not match:
            return None

        episode = int(match.group(1))

        # Title is everything before the episode marker
        title = cleaned_name[: match.start()].strip()

        # Assume season 1 if not specified
        return Episode(title, 1, episode)


class SeasonEpisodeListParser(Parser[MultiEpisode]):
    """Matches S01E01E02E03 pattern"""

    def parse(self, cleaned_name: str) -> MultiEpisode | None:
        # Match S##E##E##... pattern (case insensitive)
        pattern = r"\bs(\d{1,2})e(\d{1,2}(?:e\d{1,2})+)\b"
        match = re.search(pattern, cleaned_name, re.IGNORECASE)

        if not match:
            return None

        season = int(match.group(1))
        episodes_str = match.group(2)
        # Extract all episode numbers
        episodes = [int(ep) for ep in re.findall(r"\d+", episodes_str)]

        # Title is everything before the season/episode marker
        title = cleaned_name[: match.start()].strip()

        return MultiEpisode(title, season, episodes)


class SeasonEpisodeRangeParser(Parser[MultiEpisode]):
    """Matches S01E01-E02 pattern"""

    def parse(self, cleaned_name: str) -> MultiEpisode | None:
        # Match S##E##-E## pattern (case insensitive)
        pattern = r"\bs(\d{1,2})e(\d{1,2})-e(\d{1,2})\b"
        match = re.search(pattern, cleaned_name, re.IGNORECASE)

        if not match:
            return None

        season = int(match.group(1))
        start_ep = int(match.group(2))
        end_ep = int(match.group(3))
        episodes = list(range(start_ep, end_ep + 1))

        # Title is everything before the season/episode marker
        title = cleaned_name[: match.start()].strip()

        return MultiEpisode(title, season, episodes)
