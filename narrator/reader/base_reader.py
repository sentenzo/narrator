from narrator.article import Article


class BaseReader:
    @staticmethod
    def read_text(obj) -> Article:
        raise NotImplemented()

    @staticmethod
    def is_readable(obj) -> bool:
        raise NotImplemented()
