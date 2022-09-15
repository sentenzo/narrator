from aiogram.types import Document

from ..base_reader import BaseReader


class BaseFileReader(BaseReader):
    @staticmethod
    def read_text(obj: str) -> str:
        raise NotImplemented()

    @staticmethod
    def is_readable(obj: str) -> bool:
        raise NotImplemented()
