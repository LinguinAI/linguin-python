import unittest
import responses
from faker import Faker
from faker.providers import misc
from linguin import Linguin
from linguin import LinguinInputError

class TestBulkDetectLanguage(unittest.TestCase):
    def setUp(self):
        self.faker = Faker()
        self.faker.add_provider(misc)
        self.api_token = self.faker.uuid4()
        self.linguin = Linguin(self.api_token)
        self.input_texts = self.faker.words()
        self.url = 'https://api.linguin.ai/v2/bulk_detect/language'

    @responses.activate
    def test_bulk_success(self):
        successful_response = {'results': [[{'lang': 'en', 'confidence': 1.0}], [{'lang': 'de', 'confidence': 1.0}]]}
        responses.add(responses.POST, self.url, json=successful_response, status=200)

        response = self.linguin.bulk_detect_language(self.input_texts)

        assert response.is_success == True
        assert response.error == None
        assert response.result == successful_response
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == self.url
        assert responses.calls[0].request.headers['Authorization'] == 'Bearer {token}'.format(token=self.api_token)

        body = '&'.join(['q%5B%5D={}'.format(word) for word in self.input_texts])
        assert responses.calls[0].request.body == body

    @responses.activate
    def test_bulk_local_error(self):
        successful_response = {'results': [[{'lang': 'en', 'confidence': 1.0}], [{'lang': 'de', 'confidence': 1.0}]]}
        responses.add(responses.POST, self.url, json=successful_response, status=200)

        response = self.linguin.bulk_detect_language(['', 'test'])

        assert len(responses.calls) == 0
        assert response.is_success == False
        assert type(response.error) is LinguinInputError
        assert response.result == None

    @responses.activate
    def test_bulk_input_error(self):
        error_response = self.faker.text()
        responses.add(responses.POST, self.url, body=error_response, status=400)

        response = self.linguin.bulk_detect_language(self.input_texts)

        assert response.is_success == False
        assert type(response.error) is LinguinInputError
        assert response.result == None
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == self.url
        assert responses.calls[0].request.headers['Authorization'] == 'Bearer {token}'.format(token=self.api_token)

        body = '&'.join(['q%5B%5D={}'.format(word) for word in self.input_texts])
        assert responses.calls[0].request.body == body
