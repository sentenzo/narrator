from __future__ import annotations
import os
import datetime

from narrator.thirdparty import blb2txt, balcon, ffmpeg__to_mp3
from narrator.utils import make_filename
from narrator.exceptions import TextException
from narrator.text.language import Language

import narrator.config

conf = narrator.config.text


class Text:

    INPUT_FORMATS = conf.input_formats

    MAX_INPUT_SIZE = conf.max_input_size

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

        char_count = 0
        score = {lang.value: 0 for lang in Language}
        for ch in text:
            lang_val = Language.get_val(ch)
            if lang_val:
                score[lang_val] += 1
                if lang_val:
                    char_count += 1
                if char_count >= stop_at:
                    break
        _, max_lang_val = max((cnt, lang_val) for lang_val, cnt in score.items())
        return Language(max_lang_val)

    def __init__(
        self, title: str, paragraphs: list[str] | str, lang: Language | None = None
    ) -> None:
        self._title = title
        self._paragraphs = paragraphs
        self._lang: Language = lang or Text.guess_language(paragraphs)
        self._datetime = datetime.datetime.now()

    def _preamble(self) -> str:
        preamble = []

        preamble.append(self._title)
        if self._lang == Language.RU:
            preamble.append("Создано: " + self._datetime.strftime("%Y-%m-%d %H:%M:%S"))
        else:
            preamble.append("Created: " + self._datetime.strftime("%Y-%m-%d %H:%M:%S"))
        return "\n".join(preamble)

    def save_to_txt(
        self, directory: str, filename: str | None = None, encoding: str = "utf-8"
    ) -> str:
        if not filename:
            filename = make_filename(self._title + ".txt")
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
        text = open(file_path, encoding=encoding).read()
        filename = os.path.basename(file_path)
        title, _ = os.path.splitext(filename)
        return Text(title, text)

    def has_proper_extention(filename):
        ext = os.path.splitext(filename)[1]
        return ext.lower() in Text.INPUT_FORMATS

    @staticmethod
    def from_file(file_path: str) -> Text:
        if not Text.has_proper_extention(file_path):
            raise TextException()
        ext = os.path.splitext(file_path)[1]
        if not ext == ".txt":
            try:
                file_path = blb2txt(file_path)
            except TextException:
                raise
        return Text.from_txt(file_path)

    def save_to_mp3(self, directory: str, filename: str | None = None) -> str:
        # balcon.exe only works with UTF-8-BOM (or "utf-8-sig")
        txt_path = self.save_to_txt(directory, filename, "utf-8-sig")
        wav_path = balcon(txt_path, self._lang.value)
        mp3_path = ffmpeg__to_mp3(wav_path)
        return mp3_path
