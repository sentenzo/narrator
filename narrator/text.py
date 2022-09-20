from __future__ import annotations
from enum import Enum


class Text:
    class Language(Enum):
        ru: str = "ru"
        en: str = "en"

    def __init__(self, lang: Text.Language, paragraphs: list[str]) -> None:
        self._lang = lang
        self._paragraphs = paragraphs

    def save_to_txt(self, directory: str, filename: str | None = None) -> str:
        return "dummy"
