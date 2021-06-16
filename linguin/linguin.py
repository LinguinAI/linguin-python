import requests
from .response import Response
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

    def __init__(self, api_key):
        self.api_key = api_key
        self.headers = {
            'Authorization': 'Bearer ' + self.api_key
        }

    def detect(self, text):
        '''Returns detection response from the server and raises errors

        Parameters:
            text (string): query text for detection

        Returns:
            parsed json response (dict)
            e.g. {'results': [{'lang': 'en', 'confidence': 1.0}, {'lang': 'de', 'confidence': 0.2}]}
        '''
        text = self.__sanitize(text)

        if not text:
            raise LinguinInputError(400,
                                    'The language of an empty text is more of a philosophical question.')

        url = '{base}/{version}/detect'.format(base=self.BASE_URI, version=self.API_VERSION)
        payload = {'q': text}
        response = requests.post(url, data=payload, headers=self.headers)

        return Response.parse(response)

    def bulk(self, texts):
        '''Returns bulk detection response from the server and raises errors

        Parameters:
            texts (array of strings): query texts for bulk detection

        Returns:
            parsed json response (dict)
            e.g. [ {'results': [{'lang': 'en', 'confidence': 1.0}]},
                   {'results': [{'lang': 'de', 'confidence': 0.2}]} ]
        '''
        texts = list(map(self.__sanitize, texts))

        if any(not isinstance(text, str) or len(text) == 0 for text in texts):
            raise LinguinInputError(
                400, 'At least one of the texts provided was empty.')

        url = '{base}/{version}/bulk'.format(base=self.BASE_URI, version=self.API_VERSION)
        payload = {'q[]': texts}
        response = requests.post(url, data=payload, headers=self.headers)

        return Response.parse(response)

    def status(self):
        '''Returns api usage status from the server and raises errors

        Returns:
            parsed json response (dict)
            e.g. {'daily_limit': 10000, 'detections_today': 8000, 'remaining_today': 2000}
        '''
        url = '{base}/{version}/status'.format(
            base=self.BASE_URI, version=self.API_VERSION)
        response = requests.get(url, headers=self.headers)

        return Response.parse(response)

    @staticmethod
    def __sanitize(text):
        '''Returns text striped of white spaces '''
        return str(text).strip()
