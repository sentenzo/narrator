import urllib.request as ur
import re

from .base_url_extractor import BaseUrlExtractor


class HabrExtractor(BaseUrlExtractor):
    @staticmethod
    def extract_text(obj: str) -> str:
        return "HabrExtractor dummy"

    @staticmethod
    def is_extractable(obj: str) -> bool:
        if re.match(r"https\://habr\.com/../post/\d+", obj):
            return BaseUrlExtractor.is_extractable(obj)
        else:
            return False
