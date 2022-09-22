from urllib.parse import urlparse
from urllib.request import urlopen
import re

from bs4 import BeautifulSoup

from narrator.exceptions import UrlInvalid, UrlUnreachable, ParsingRulesNotFound
from narrator.text.text import Text
import narrator.config

conf = narrator.config.web_parser

# https://stackoverflow.com/a/38020041/2493536
def is_uri_valid(maybe_url: str) -> bool:
    try:
        result = urlparse(maybe_url)
        return all([result.scheme, result.netloc])
    except:
        return False


def is_url_reachable(url: str, timeout=3) -> bool:
    try:
        with urlopen(url, timeout=timeout):
            return True
    except Exception:
        return False


class Url:
    def __init__(self, url: str) -> None:
        self._url = url

        self._is_valid: bool | None = None
        self._is_reachable: bool | None = None
        self._parsed_text: Text | None = None

    @property
    def is_valid(self) -> bool:
        if self._is_valid == None:
            self._is_valid = is_uri_valid(self._url)
        return self._is_valid

    @property
    def is_reachable(self) -> bool:
        if self._is_reachable == None:
            self._is_reachable = is_url_reachable(self._url)
        return self._is_reachable

    def _get_html(self) -> str:
        with urlopen(self._url) as resp:
            html = resp.read().decode()
            return html

    def _pick_parse_config(self):
        for site in conf.sites:
            if re.match(conf.sites[site].url_re, self._url):
                return conf.sites[site]
        return None

    def parse(self) -> Text:
        if not self.is_valid:
            raise UrlInvalid()
        if not self.is_reachable:
            raise UrlUnreachable()

        if not self._parsed_text:
            html = self._get_html()
            soup = BeautifulSoup(html, "html.parser")
            parse_config = self._pick_parse_config()
            if not parse_config:
                raise ParsingRulesNotFound(
                    f"The rules to parse {self._url} are not specified in the config file"
                )
            title = soup.select_one(parse_config.re.title).text.strip()
            author = soup.select_one(parse_config.re.author).text.strip()
            publication_date: str = soup.select_one(
                parse_config.re.publication_date
            ).text.strip()

            paragraphs = []
            paragraphs.append(f"author: {author}")
            paragraphs.append(f"publication_date: {publication_date}")
            paragraphs.append(soup.select_one(parse_config.re.text).text)

            self._parsed_text = Text(title, paragraphs)
        return self._parsed_text
