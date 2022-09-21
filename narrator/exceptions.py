class NarratorException(Exception):
    """
    Base class for any Narrator exception
    """


class UrlParserException(NarratorException):
    pass


class UrlInvalid(UrlParserException):
    pass


class UrlUnreachable(UrlParserException):
    pass


class TxtTransformerException(NarratorException):
    pass