from urllib.parse import urlparse
from urllib.request import urlopen

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
    """
    dummy
    """

    def __init__(self, url: str) -> None:
        self._url = url

        self._is_valid: bool | None = None
        self._is_reachable: bool | None = None
        self._parsed_text: list[str] | None = None

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

    def parse(self) -> list[str]:
        raise NotImplemented()
        if not self._parsed_text:
            ...
            # self._parsed_text = something
        return self._parsed_text
