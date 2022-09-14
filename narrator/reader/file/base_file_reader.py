from ..base_reader import BaseReader


class BaseFileReader(BaseReader):
    @staticmethod
    def read_text(obj) -> str:
        raise NotImplemented()

    @staticmethod
    def is_readable(obj) -> bool:
        return False
