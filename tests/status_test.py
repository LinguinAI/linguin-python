import unittest
import responses
from faker import Faker
from faker.providers import misc
from linguin import Linguin

class TestStatus(unittest.TestCase):
    def setUp(self):
        self.faker = Faker()
        self.faker.add_provider(misc)
        self.api_token = self.faker.uuid4()
        self.linguin = Linguin(self.api_token)

    @responses.activate
    def test_status(self):
        successful_response = {'daily_limit': -1, 'detections_today': None, 'remaining_today': -1}
        url = 'https://api.linguin.ai/v1/status'
        responses.add(responses.GET, url, json=successful_response, status=200)

        response = self.linguin.status()

        assert response == successful_response
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == url
        assert responses.calls[0].request.headers['Authorization'] == 'Bearer {token}'.format(token=self.api_token)
