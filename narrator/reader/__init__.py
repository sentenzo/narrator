"""
Tools to convert input to txt, suitable for reading
"""
from . import file, url


def from_file(obj) -> str:
    return file.read_text(obj)


def from_url(obj) -> str:
    return url.read_text(obj)


__all__ = [from_file, from_url]