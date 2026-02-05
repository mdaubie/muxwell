from dataclasses import dataclass

import typer


@dataclass
class IdLangPair:
    track_id: int
    lang: str

    @classmethod
    def parse(cls, value: str) -> "IdLangPair":
        try:
            track_id_str, lang = value.split(":", 1)
        except ValueError as e:
            raise typer.BadParameter(
                f"Invalid format: '{value}'. Expected '<track_id>:<lang>'."
            ) from e
        return cls(int(track_id_str), lang)
