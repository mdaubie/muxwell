from __future__ import annotations

from dataclasses import dataclass

import typer

from ..mkv.models import TrackSelector, TypeLangTrackSelector


@dataclass
class IdLangPair:
    track_id: int
    lang: str

    FORMAT = "<track_id>:<lang>"
    FORMAT_EXAMPLE = "1:eng"

    @classmethod
    def parse(cls, value: str) -> IdLangPair:
        try:
            track_id_str, lang = value.split(":", 1)
        except ValueError as e:
            raise typer.BadParameter(
                f"Invalid format: '{value}'. Expected '{cls.FORMAT}'."
            ) from e
        return cls(int(track_id_str), lang)


@dataclass
class TrackSelectorArg:
    value: TrackSelector

    FORMAT = "<track_id> | <type>:<lang>"
    FORMAT_EXAMPLE = "1 | audio:eng"

    @classmethod
    def parse(cls, value: str) -> TrackSelectorArg:
        if value.isdigit():
            return TrackSelectorArg(int(value))
        else:
            try:
                return TrackSelectorArg(_parse_type_lang_track_selector(value))
            except ValueError as e:
                raise typer.BadParameter(
                    f"Invalid format: '{value}'. Expected '{TrackSelectorArg.FORMAT}'."
                ) from e


def _parse_type_lang_track_selector(value: str) -> TypeLangTrackSelector:
    try:
        type, lang = value.split(":", 1)
    except ValueError as e:
        raise typer.BadParameter(
            f"Invalid format: '{value}'. Expected '<type>:<lang>'."
        ) from e
    if type not in ("video", "audio", "subs", "subtitles"):
        raise typer.BadParameter(
            f"Invalid track type: '{type}'. Expected one of 'video', 'audio', 'subs', 'subtitles'."
        )
    type = "subtitles" if type == "subs" else type
    return TypeLangTrackSelector(type, lang)
