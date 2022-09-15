import re
from urllib.request import urlopen
from urllib.parse import urlparse

from narrator.article import Article
from ..base_reader import BaseReader

# https://stackoverflow.com/a/38020041/2493536
def _uri_validator(x):
    try:
        result = urlparse(x)
        return all([result.scheme, result.netloc])
    except:
        return False


class BaseUrlReader(BaseReader):
    @staticmethod
    def read_text(obj: str) -> Article:
        raise NotImplemented()

    @staticmethod
    def is_readable(obj: str) -> bool:
        return _uri_validator(obj)

    @staticmethod
    def _re_check_url(re_temp: str, url: str) -> bool:
        if re.match(re_temp, url):
            return True
        else:
            return False

    @staticmethod
    def get_html(url: str) -> str:
        with urlopen(url) as resp:
            html = resp.read().decode()
            return html
