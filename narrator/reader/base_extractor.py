class BaseExtructor:
    @staticmethod
    def extract_text(obj) -> str:
        raise NotImplemented()

    @staticmethod
    def is_extractable(obj) -> bool:
        raise NotImplemented()
