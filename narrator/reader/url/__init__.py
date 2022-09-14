import urllib.request as ur

from .habr_reader import HabrReader
from .base_url_reader import BaseUrlReader

URL_EXTRUCTORS = [HabrReader]


def read_text(obj: str) -> str:
    for Extr in URL_EXTRUCTORS:
        if Extr.is_readable(obj):
            return Extr.read_text(obj)
    return f"No reader matches the url: {obj}"


def is_url(obj: str) -> bool:
    return BaseUrlReader.is_readable(obj)


__all__ = [read_text, is_url]