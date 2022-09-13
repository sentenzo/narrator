from urllib.parse import urlparse

from ..base_extractor import BaseExtructor

# https://stackoverflow.com/a/38020041/2493536
def uri_validator(x):
    try:
        result = urlparse(x)
        return all([result.scheme, result.netloc])
    except:
        return False


class BaseUrlExtractor(BaseExtructor):
    @staticmethod
    def extract_text(obj: str) -> str:
        raise NotImplemented()

    @staticmethod
    def is_extractable(obj: str) -> bool:
        return uri_validator(obj)
