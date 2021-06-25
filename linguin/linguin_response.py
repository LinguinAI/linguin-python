from .exceptions import LinguinInputError
from .exceptions import LinguinAuthenticationError
from .exceptions import LinguinNotFoundError
from .exceptions import LinguinRateLimitError
from .exceptions import LinguinInternalError
from .exceptions import LinguinUnknownError


class LinguinResponse:
    """Wrapper class for Linguin API response

    Attributes:
        - is_success: bool - whether the call was successful
        - error: LinguinError object containing status code and message
        - result: parsed json response (dict)
        e.g. {'results': [{'lang': 'en', 'confidence': 1.0}, {'lang': 'de', 'confidence': 0.2}]}
    """

    ERROR_CLS_MAP = {
        400: LinguinInputError,
        401: LinguinAuthenticationError,
        404: LinguinNotFoundError,
        422: LinguinInputError,
        429: LinguinRateLimitError,
        500: LinguinInternalError,
        503: LinguinInternalError
    }

    def __build_error(self, response):
        error_class = self.ERROR_CLS_MAP.get(response.status_code)

        if error_class:
            return error_class(response.status_code, response.text)
        else:
            return LinguinUnknownError(response.status_code, response.text)

    def __init__(self, response=None, error=None):
        if response is not None:
            self.is_success = response.status_code == 200
            self.error = None if self.is_success else self.__build_error(response)
            self.result = response.json() if self.is_success else None

        if error is not None:
            self.is_success = False
            self.error = error
            self.result = None

    def raise_on_error(self):
        '''Call this method to raise a LinguinError after initializing the response'''

        if self.error:
            raise self.error
