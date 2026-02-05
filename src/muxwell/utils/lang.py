from __future__ import annotations

import typer
from iso639 import Language, LanguageNotFoundError


def normalize_language(code: str) -> str:
    """
    Normalize a language identifier to a 3-letter ISO-639-2/B code.

    :param code: A language identifier (e.g., 'en', 'eng', 'fra', 'fre', 'French' etc.)
    :type code: str
    :return: A normalized 3-letter ISO-639-2/B language code.
    :rtype: str
    :raises typer.BadParameter: if the language cannot be resolved.
    """
    try:
        lang = Language.match(code, strict_case=False)
        if not lang.part2b:
            raise typer.BadParameter(f"Invalid language code: {code}")
        return lang.part2b
    except LanguageNotFoundError as e:
        raise typer.BadParameter(f"Invalid language code: {code}") from e
