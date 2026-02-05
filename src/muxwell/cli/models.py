from __future__ import annotations

from dataclasses import dataclass

import typer


@dataclass
class IdLangPair:
    track_id: int
    lang: str

    @classmethod
    def parse(cls, value: str) -> IdLangPair:
        try:
            track_id_str, lang = value.split(":", 1)
        except ValueError as e:
            raise typer.BadParameter(
                f"Invalid format: '{value}'. Expected '<track_id>:<lang>'."
            ) from e
        return cls(int(track_id_str), lang)


@dataclass
class IdDefaultPair:
    track_id: int
    default: bool

    @classmethod
    def parse(cls, value: str) -> IdDefaultPair:
        try:
            track_id_str, default_str = value.split(":", 1)
        except ValueError as e:
            raise typer.BadParameter(
                f"Invalid format: '{value}'. Expected '<track_id>:<0|1>'."
            ) from e
        if default_str not in ("0", "1"):
            raise typer.BadParameter(
                f"Invalid default flag: '{default_str}'. Expected '0' or '1'."
            )
        return cls(int(track_id_str), default_str == "1")
