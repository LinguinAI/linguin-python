import requests
from .linguin_response import LinguinResponse
from .exceptions import LinguinInputError


class Linguin:
    """Client class for Linguin API

    Supported endpoints:
        /detect
        /bulk
        /status
    """

    API_VERSION = 'v1'
    BASE_URI = 'https://api.linguin.ai'

    def __init__(self, api_key, raise_on_error=False):
        self.api_key = api_key
        self.headers = {
            'Authorization': 'Bearer ' + self.api_key
        }
        self.raise_on_error = raise_on_error

    def detect(self, text, raise_on_error=False):
        '''Returns detection response from the server and raises errors

        Parameters:
            text (string): query text for detection

        Returns:
            a LinguinResponse object containing
            parsed json response (dict)
            e.g. {'results': [{'lang': 'en', 'confidence': 1.0}, {'lang': 'de', 'confidence': 0.2}]}
        '''
        text = self.__sanitize(text)

        if not text:
            error = LinguinInputError(400, 'The language of an empty text is more of a philosophical question.')
            return LinguinResponse(error=error)

        url = '{base}/{version}/detect'.format(base=self.BASE_URI, version=self.API_VERSION)
        payload = {'q': text}
        response = requests.post(url, data=payload, headers=self.headers)
        # import code; code.interact(local=dict(globals(), **locals()))
        if raise_on_error or self.raise_on_error: response.raise_on_error()

        return LinguinResponse(response=response)


    def bulk(self, texts, raise_on_error=False):
        '''Returns bulk detection response from the server and raises errors

        Parameters:
            texts (array of strings): query texts for bulk detection

        Returns:
            a LinguinResponse object containing
            parsed json response (dict)
            e.g. [ {'results': [{'lang': 'en', 'confidence': 1.0}]},
                   {'results': [{'lang': 'de', 'confidence': 0.2}]} ]
        '''
        texts = list(map(self.__sanitize, texts))

        if any(not isinstance(text, str) or len(text) == 0 for text in texts):
            error = LinguinInputError(400, 'At least one of the texts provided was empty.')
            return LinguinResponse(error=error)

        url = '{base}/{version}/bulk'.format(base=self.BASE_URI, version=self.API_VERSION)
        payload = {'q[]': texts}
        response = requests.post(url, data=payload, headers=self.headers)
        if raise_on_error or self.raise_on_error: response.raise_on_error()

        return LinguinResponse(response)

    def status(self, raise_on_error=False):
        '''Returns api usage status from the server and raises errors

        Returns:
            a LinguinResponse object containing
            parsed json response (dict)
            e.g. {'daily_limit': 10000, 'detections_today': 8000, 'remaining_today': 2000}
        '''
        url = '{base}/{version}/status'.format(base=self.BASE_URI, version=self.API_VERSION)
        response = requests.get(url, headers=self.headers)
        if raise_on_error or self.raise_on_error: response.raise_on_error()

        return LinguinResponse(response)

    @staticmethod
    def __sanitize(text):
        '''Returns text striped of white spaces '''
        return str(text).strip()
