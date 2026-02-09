from __future__ import annotations

import re
from functools import lru_cache

from .patterns import (
    EpisodeOnlyParser,
    MovieYearParser,
    SeasonEpisodeCompactParser,
    SeasonEpisodeListParser,
    SeasonEpisodeRangeParser,
    SeasonEpisodeXParser,
)

parsers = [
    SeasonEpisodeListParser(),
    SeasonEpisodeRangeParser(),
    SeasonEpisodeCompactParser(),
    SeasonEpisodeXParser(),
    EpisodeOnlyParser(),
    MovieYearParser(),
]


@lru_cache
def parse_filename(filename: str):
    cleaned = _preprocess(filename)
    for parser in parsers:
        if result := parser.parse(cleaned):
            return result
    return None


def _preprocess(filename: str) -> str:
    """
    Clean and normalize a filename for parsing.
    1. Remove file extension
    2. Strip common tags (quality, codec, source, etc.)
    3. Normalize separators
    """
    # Remove extension
    name = re.sub(r"\.[^.]*$", "", filename)

    # Remove common quality/codec/source tags (case insensitive)
    # Ordered roughly by frequency
    tags_to_remove = [
        # Resolutions
        r"\b\d{3,4}p\b",
        r"\b(?:HD|SD|UHD|4K|8K)\b",
        r"\b(?:720|1080|2160|4320)\b",
        # Codecs
        r"\b(?:x264|x265|xvid|h\.?264|h\.?265|hevc|av1|vp9)\b",
        r"\b(?:8bit|10bit|12bit)\b",
        # Sources
        r"\b(?:BluRay|Blu\-Ray|BDRip|BRRip|DVDRip|HDTV|PDTV|DSR|WEB\-DL|WEBRip|WEB)\b",
        # Audio
        r"\b(?:AAC2\.0|AC3|DTS|DD5\.1|DDP5\.1|DD\+5\.1|Atmos)\b",
        r"\b(?:\d+CH)\b",
        # Other common tags
        r"\b(?:REMUX|PROPER|REPACK|READNFO|NFO|RARBG)\b",
        r"\b(?:Extended|Unrated|Director\'s\.Cut|Theatrical\.Cut)\b",
        # HDR variants
        r"\b(?:HDR|HDR10\+|DV|Dolby\.Vision)\b",
        # Streaming services
        r"\b(?:NF|AMZN|DSNP|HMAX|ATVP)\b",
        # Tracker/website tags in brackets (e.g., [eztv.re], [rarbg])
        r"\[[\w\.\-]+\]",
        # Release groups (typically at the end after a hyphen)
        r"\-[A-Z0-9]+$",
    ]

    for pattern in tags_to_remove:
        name = re.sub(pattern, "", name, flags=re.IGNORECASE)

    # Normalize separators: replace dots, underscores, brackets, parentheses with spaces
    name = re.sub(r"[._\[\]()]", " ", name)

    # Replace hyphens with spaces only if they're surrounded by spaces (separators)
    name = re.sub(r"\s+-+\s+", " ", name)

    # Collapse multiple spaces and trim
    name = re.sub(r"\s+", " ", name).strip()

    return name
