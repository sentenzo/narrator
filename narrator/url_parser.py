class Url:
    """
    dummy
    """

    def __init__(self, url: str) -> None:
        self._url = url
        self._parsed_text: list[str] | None = None

    def is_valid(self) -> bool:
        return False

    def is_reachable(self) -> bool:
        return False

    def parse(self) -> list[str]:
        raise NotImplemented()
        if not self._parsed_text:
            ...
            # self._parsed_text = something
        return self._parsed_text
