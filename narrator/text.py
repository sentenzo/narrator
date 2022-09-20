from __future__ import annotations
import os
from enum import Enum
import string
import datetime


class Text:
    class Language(Enum):
        # def __init__(self, char_set, name) -> None:

        RU: str = "ru"
        EN: str = "en"

    @staticmethod
    def guess_language(text: str | list[str]) -> Language:
        stop_at = 1000
        if isinstance(text, list):
            acc = 0
            to_join = []
            for par in text:
                acc += len(par)
                to_join.append(par)
                if acc >= stop_at:
                    break
            text = "".join(to_join)

        en_set = string.ascii_letters
        ru_set = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
        ru_set += ru_set.upper()

        char_count = 0
        score = {"en": 0, "ru": 0}
        for ch in text:
            if ch in en_set:
                score["en"] += 1
                char_count += 1
            elif ch in ru_set:
                score["ru"] += 1
                char_count += 1
            if char_count >= stop_at:
                break
        return Text.Language.EN if score["en"] >= score["ru"] else Text.Language.RU

    def __init__(
        self, title: str, paragraphs: list[str] | str, lang: Text.Language | None = None
    ) -> None:
        self._title = title
        self._paragraphs = paragraphs
        self._lang: Text.Language = lang or Text.guess_language(paragraphs)
        self._datetime = datetime.datetime.now()

    def _preamble(self) -> str:
        preamble = []

        preamble.append(self._title)
        if self._lang == Text.Language.RU:
            preamble.append("Создано: " + self._datetime.strftime("%Y-%m-%d %H:%M:%S"))
        else:
            preamble.append("Created: " + self._datetime.strftime("%Y-%m-%d %H:%M:%S"))
        return "\n".join(preamble)

    def save_to_txt(
        self, directory: str, filename: str | None = None, encoding: str = "utf-8"
    ) -> str:
        if not filename:
            filename = self._title + ".txt"
        file_path = os.path.join(directory, filename)
        with open(file_path, mode="w", encoding=encoding) as txt:  # utf-8-sig
            txt.write(self._preamble() + "\n")
            if isinstance(self._paragraphs, list):
                for p in self._paragraphs:
                    txt.write(p + "\n")
            elif isinstance(self._paragraphs, str):
                txt.write(self._paragraphs)
        return file_path

    @staticmethod
    def from_txt(file_path: str, encoding: str = "utf-8") -> Text:
        text = open(file_path, encoding="utf-8").read()
        filename = os.path.basename(file_path)
        title, _ = os.path.splitext(filename)
        return Text(title, text)
