"""All exceptions for Linguin API"""


class LinguinError(Exception):
    """Base class for Linguin errors"""

    def __init__(self, status, message):
        self.status = status
        self.message = message

    def __str__(self):
        return 'Error code: {status}. {message}'.format(status=self.status, message=self.message)


class LinguinInputError(LinguinError):
    pass


class LinguinNotFoundError(LinguinError):
    pass


class LinguinAuthenticationError(LinguinError):
    pass


class LinguinRateLimitError(LinguinError):
    pass


class LinguinInternalError(LinguinError):
    pass


class LinguinUnknownError(LinguinError):
    pass
