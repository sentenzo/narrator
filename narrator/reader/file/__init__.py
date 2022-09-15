from aiogram.types import Document

from narrator.article import Article
from .txt_reader import TxtReader
from .base_file_reader import BaseFileReader

FILE_READERS = [TxtReader]


def read_text(file_path: str) -> Article:
    for Reader in FILE_READERS:
        if Reader.is_readable(file_path):
            return Reader.read_text(file_path)
    return f"No reader matches the file: {file_path}"


def is_readable_ext(file_name: str) -> bool:
    for Reader in FILE_READERS:
        if Reader.is_readable(file_name):
            return True
    return False


__all__ = [read_text, is_readable_ext]
