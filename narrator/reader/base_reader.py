class BaseReader:
    @staticmethod
    def read_text(obj) -> str:
        raise NotImplemented()

    @staticmethod
    def is_readable(obj) -> bool:
        raise NotImplemented()
