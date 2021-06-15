"""All exceptions for Linguin API"""

class LinguinError(Exception):
    """Base class for Linguin errors"""

    message = 'Error code: {status}. {content}'

    def __init__(self, status, content):
        self.status = status
        self.content = content

    def __str__(self):
        return self.message.format(status=self.status, content=self.content)

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
