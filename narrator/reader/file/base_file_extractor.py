from ..base_extractor import BaseExtructor


class BaseFileExtractor(BaseExtructor):
    @staticmethod
    def extract_text(obj) -> str:
        raise NotImplemented()

    @staticmethod
    def is_extractable(obj) -> bool:
        return False
