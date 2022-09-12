import urllib.request as ur


class UrlToText:
    @staticmethod
    def url_to_txt(url: str) -> str:
        raise NotImplemented()


class HarbToText(UrlToText):
    @staticmethod
    def url_to_txt(url: str) -> str:
        # ur.urlopen()
        return "dummy"


__all__ = (UrlToText, HarbToText)
