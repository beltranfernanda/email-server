import unittest

from flask import Flask

from app.controller.ping import PingController


class TestPingController(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app.testing = True
        self.app.add_url_rule('/ping', view_func=PingController().ping)
        self.client = self.app.test_client()

    def test_ping(self):
        response = self.client.get('/ping')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'message': 'pong'})