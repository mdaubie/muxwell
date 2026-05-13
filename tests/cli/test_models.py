"""Tests for muxwell.cli.models module."""

from __future__ import annotations

import pytest
import typer

from muxwell.cli.models import TrackSelectorArg, TypeLangTrackSelector


class TestTrackSelectorArg:
    """Tests for TrackSelectorArg parsing and ordering."""

    def test_parse_integer(self):
        selector = TrackSelectorArg.parse("12")
        assert selector.value == 12

    def test_parse_type_lang(self):
        selector = TrackSelectorArg.parse("audio:eng")
        assert isinstance(selector.value, TypeLangTrackSelector)
        assert selector.value.type == "audio"
        assert selector.value.lang == "eng"

    @pytest.mark.parametrize(
        "value",
        [
            pytest.param("abc", id="not_integer_or_selector"),
            pytest.param("audio-eng", id="wrong_separator"),
        ],
    )
    def test_parse_invalid_format(self, value: str):
        with pytest.raises(typer.BadParameter, match="Invalid format"):
            TrackSelectorArg.parse(value)

    def test_parse_invalid_type(self):
        with pytest.raises(typer.BadParameter, match="Invalid track type"):
            TrackSelectorArg.parse("text:eng")
