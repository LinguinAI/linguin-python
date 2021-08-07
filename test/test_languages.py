import unittest
import responses
from linguin import Linguin

class TestLanguages(unittest.TestCase):
    def setUp(self):
        self.url = 'https://api.linguin.ai/v2/languages'

    @responses.activate
    def test_languages(self):
        successful_response = {'ab': ['Abkhazian', 'аҧсуа бызшәа, аҧсшәа'], 'af': ['Afrikaans', 'Afrikaans']}
        responses.add(responses.GET, self.url, json=successful_response, status=200)

        languages = Linguin.languages()
        assert languages == successful_response
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == self.url
