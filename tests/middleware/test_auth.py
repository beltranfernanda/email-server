import unittest
from unittest.mock import Mock

from flask import Flask

from app.middleware.auth import AuthMiddleware
from tests.utils.magic_mock_with_name import MagicMockWithName


class TestAuthMiddleware(unittest.TestCase):
    def setUp(self):
        self.mock_view_func = MagicMockWithName(return_value="view_response")
        self.mock_config = Mock()
        self.mock_config.get_param = Mock(return_value="develop")
        self.app = Flask(__name__)
        self.app.testing = True
        self.app.add_url_rule(
            "/middleware",
            view_func=AuthMiddleware(self.mock_view_func, self.mock_config),
            methods=["GET"],
        )
        self.client = self.app.test_client()

    def test_missing_authorization_header(self):
        response = self.client.get("/middleware")
        self.assertEqual(response.status_code, 401)

    def test_invalid_hmac_signature(self):
        response = self.client.get("/middleware", headers={"Authorization": "test"})
        self.assertEqual(403, response.status_code)

    def test_valid_hmac_signature_and_view_func_call(self):
        response = self.client.get(
            "/middleware",
            headers={
                "Authorization": "jLGma3E97LZn+GeTISWgfxeViLAkTBqf2vwPQbeEbqc=",
                "x-origin": "test",
            },
        )
        self.assertEqual(200, response.status_code)
