class NarratorException(Exception):
    """
    Base class for any Narrator exception
    """


class UrlParserException(NarratorException):
    pass


class TxtTransformerException(NarratorException):
    pass
