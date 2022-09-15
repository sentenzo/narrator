import os

from aiogram.types import Document

from narrator.article import Article
from .base_file_reader import BaseFileReader


class TxtReader(BaseFileReader):
    @staticmethod
    def read_text(obj: str) -> Article:
        article = Article()
        article["file name"] = obj  # os.path.splitext(obj)[0]

        return article

    @staticmethod
    def is_readable(obj: str) -> bool:
        return os.path.splitext(obj)[1] == ".txt"
