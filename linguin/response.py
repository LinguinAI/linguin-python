from .exceptions import *

class Response:
    CODE_MAP = {
        400: LinguinInputError,
        401: LinguinAuthenticationError,
        404: LinguinNotFoundError,
        422: LinguinInputError,
        429: LinguinRateLimitError,
        500: LinguinInternalError,
        503: LinguinInternalError
    }

    @classmethod
    def parse(cls, response):
        if response.status_code == 200:
            return response.json()
        else:
            raise cls.CODE_MAP[response.status_code](response.status_code, response.text)

