import urllib.request as ur

from narrator.article import Article

from .habr_reader import HabrReader
from .base_url_reader import BaseUrlReader

URL_READERS = [HabrReader]


def read_text(obj: str) -> Article:
    for Reader in URL_READERS:
        if Reader.is_readable(obj):
            return Reader.read_text(obj)
    return f"No reader matches the url: {obj}"


def is_url(obj: str) -> bool:
    return BaseUrlReader.is_readable(obj)


__all__ = [read_text, is_url]
