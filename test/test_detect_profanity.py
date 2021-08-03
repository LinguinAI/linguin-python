import unittest
import responses
from faker import Faker
from faker.providers import misc
from linguin import Linguin
from linguin import LinguinInputError

class TestDetectProfanity(unittest.TestCase):
    def setUp(self):
        self.faker = Faker()
        self.faker.add_provider(misc)
        self.api_token = self.faker.uuid4()
        self.linguin = Linguin(self.api_token)
        self.input_text = self.faker.word()
        self.url = 'https://api.linguin.ai/v2/detect/profanity'

    @responses.activate
    def test_detect_success(self):
        successful_response = {'score': 1.0}
        responses.add(responses.POST, self.url, json=successful_response, status=200)

        response = self.linguin.detect_profanity(self.input_text)

        assert response.is_success == True
        assert response.error == None
        assert response.result == successful_response
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == self.url
        assert responses.calls[0].request.headers['Authorization'] == 'Bearer {token}'.format(token=self.api_token)
        assert responses.calls[0].request.body == 'q={input}'.format(input=self.input_text)

    @responses.activate
    def test_detect_local_error(self):
        successful_response = {'score': 1.0}
        responses.add(responses.POST, self.url, json=successful_response, status=200)

        response = self.linguin.detect_profanity(' ')

        assert len(responses.calls) == 0
        assert response.is_success == False
        assert type(response.error) is LinguinInputError
        assert response.result == None

    @responses.activate
    def test_detect_input_error(self):
        error_response = self.faker.text()
        responses.add(responses.POST, self.url, body=error_response, status=400)

        response = self.linguin.detect_profanity(self.input_text)

        assert response.is_success == False
        assert type(response.error) is LinguinInputError
        assert response.result == None
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == self.url
        assert responses.calls[0].request.headers['Authorization'] == 'Bearer {token}'.format(token=self.api_token)
        assert responses.calls[0].request.body == 'q={input}'.format(input=self.input_text)
