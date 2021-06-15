import requests
import logging
import json
from .response import Response
from .exceptions import LinguinInputError

class Linguin:
    API_VERSION = 'v1'
    BASE_URI = 'https://api.linguin.ai'

    def __init__(self, api_key):
        self.api_key = api_key
        self.headers = {
            'Authorization': 'Bearer ' + self.api_key
        }

    def detect(self, text):
        text = self.__sanitize(text)

        if not text: raise LinguinInputError(400, 'The language of an empty text is more of a philosophical question.')

        url = '{base}/{version}/detect'.format(base=self.BASE_URI, version=self.API_VERSION)
        payload = { 'q': text }
        r = requests.post(url, files=payload, headers=self.headers)

        return Response.parse(r)

    def bulk(self, texts):
        texts = list(map(lambda text: self.__sanitize(text), texts))

        if any(type(text) != str or len(text) == 0 for text in texts):
            raise LinguinInputError(400, 'At least one of the texts provided was empty.')

        url = '{base}/{version}/bulk'.format(base=self.BASE_URI, version=self.API_VERSION)
        payload = { 'q[]': texts }
        r = requests.post(url, data=payload, headers=self.headers)

        return Response.parse(r)

    def status(self):
        url = '{base}/{version}/status'.format(base=self.BASE_URI, version=self.API_VERSION)
        r = requests.get(url, headers=self.headers)

        return Response.parse(r)

    @staticmethod
    def __sanitize(text):
        return str(text).strip()
