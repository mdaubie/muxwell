"""Shared test fixtures for subtitles tests."""

from __future__ import annotations

from pathlib import Path

import pytest

from .files import FileFactory


@pytest.fixture
def subs_file(request: pytest.FixtureRequest, file_factory: FileFactory) -> Path:
    """Create a subtitle file of the requested type (srt by default)."""
    param: dict[str, str] = getattr(request, "param", {})
    ext: str = param.get("ext", "srt")
    encoding = param.get("encoding", "utf-8")
    content = CONTENT_BY_EXT.get(ext)
    if content is None:
        raise ValueError(f"Unsupported file type: {ext}")
    return file_factory(ext=ext, content=content, encoding=encoding)


@pytest.fixture
def srt_file(file_factory: FileFactory) -> Path:
    """Create an SRT subtitle file."""
    return file_factory(ext="srt", content=CONTENT_BY_EXT["srt"])


@pytest.fixture
def ssa_file(file_factory: FileFactory) -> Path:
    """Create an SSA subtitle file."""
    return file_factory(ext="ssa", content=CONTENT_BY_EXT["ssa"])


@pytest.fixture
def ass_file(file_factory: FileFactory) -> Path:
    """Create an ASS subtitle file."""
    return file_factory(ext="ass", content=CONTENT_BY_EXT["ass"])


@pytest.fixture
def subs_files(srt_file: Path, ssa_file: Path, ass_file: Path) -> list[Path]:
    """Create a list of multiple subtitle files."""
    return [srt_file, ssa_file, ass_file]


@pytest.fixture
def nested_srt_files(file_factory: FileFactory) -> list[Path]:
    """Create one SRT in root and one in nested directory."""
    root_file = file_factory(ext="srt", content=CONTENT_BY_EXT["srt"])
    nested_file = file_factory(ext="srt", content=CONTENT_BY_EXT["srt"], nested=True)
    return [root_file, nested_file]


@pytest.fixture
def invalid_srt_file(file_factory: FileFactory) -> Path:
    """Create an invalid SRT file that cannot be parsed."""
    content = "This is not a valid subtitle file."
    return file_factory(ext="srt", content=content)


CONTENT_BY_EXT = {
    "srt": """
1
00:00:01,000 --> 00:00:03,000
First subtitle
2
00:00:05,000 --> 00:00:07,500
Second subtitle
3
00:00:10,000 --> 00:00:12,000
Third subtitle with special chars: café
""",
    "ass": """
[Script Info]
Title: Test Subtitles
ScriptType: v4.00+

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial,20,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,2,0,2,10,10,10,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,0:00:01.00,0:00:03.00,Default,,0,0,0,,First subtitle
Dialogue: 0,0:00:05.00,0:00:07.50,Default,,0,0,0,,Second subtitle
Dialogue: 0,0:00:10.00,0:00:12.00,Default,,0,0,0,,Third subtitle with special chars: café
""",
    "ssa": """
[Script Info]
Title: Test Subtitles

[V4 Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, TertiaryColour, BackColour, Bold, Italic, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, AlphaLevel, Encoding
Style: Default,Arial,20,16777215,65535,65535,0,-1,0,1,3,0,2,30,30,30,0,0

[Events]
Format: Marked, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: Marked=0,0:00:01.00,0:00:03.00,Default,,0,0,0,,First subtitle
Dialogue: Marked=0,0:00:05.00,0:00:07.50,Default,,0,0,0,,Second subtitle
Dialogue: Marked=0,0:00:10.00,0:00:12.00,Default,,0,0,0,,Third subtitle with special chars: café
""",
}
