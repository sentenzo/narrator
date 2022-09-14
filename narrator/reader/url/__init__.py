import urllib.request as ur

from .habr_extractor import HabrExtractor
from .base_url_extractor import BaseUrlExtractor

URL_EXTRUCTORS = [HabrExtractor]


def extract_text(obj: str) -> str:
    for Extr in URL_EXTRUCTORS:
        if Extr.is_extractable(obj):
            return Extr.extract_text(obj)
    return f"No extractor matches the url: {obj}"


def is_url(obj: str) -> bool:
    return BaseUrlExtractor.is_extractable(obj)


__all__ = [extract_text, is_url]
