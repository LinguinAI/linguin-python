import unittest
import responses
from faker import Faker
from faker.providers import misc
from linguin import Linguin
from linguin import LinguinAuthenticationError

class TestStatus(unittest.TestCase):
    def setUp(self):
        self.faker = Faker()
        self.faker.add_provider(misc)
        self.api_token = self.faker.uuid4()
        self.linguin = Linguin(self.api_token)
        self.url = 'https://api.linguin.ai/v2/status'

    @responses.activate
    def test_status_success(self):
        successful_response = {'daily_limit': -1, 'detections_today': None, 'remaining_today': -1}
        responses.add(responses.GET, self.url, json=successful_response, status=200)

        response = self.linguin.status()

        assert response.is_success == True
        assert response.error == None
        assert response.result == successful_response
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == self.url
        assert responses.calls[0].request.headers['Authorization'] == 'Bearer {token}'.format(token=self.api_token)

    @responses.activate
    def test_status_error(self):
        error_response = self.faker.text()
        responses.add(responses.GET, self.url, body=error_response, status=401)

        response = self.linguin.status()

        assert response.is_success == False
        assert type(response.error) is LinguinAuthenticationError
        assert response.result == None
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == self.url
        assert responses.calls[0].request.headers['Authorization'] == 'Bearer {token}'.format(token=self.api_token)
