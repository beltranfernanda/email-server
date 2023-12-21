import unittest
from unittest.mock import MagicMock

from flask import Flask

from app.controller.mail import EmailController
from app.exception.email_internal_error_exception import EmailInternalErrorException


class TestEmailController(unittest.TestCase):

    def setUp(self):
        self.email_service_mock = MagicMock()
        self.app = Flask(__name__)
        self.app.testing = True
        self.app.add_url_rule('/mail/send',
                              view_func=EmailController(self.email_service_mock).send_mail, methods=['POST'])
        self.client = self.app.test_client()

    def test_send_email(self):
        # Act
        response = self.client.post('/mail/send', json={
            "name": "Test",
            "email": "test@test.com",
            "phone": "123456789",
            "message": "Test email"})
        # Assert
        assert response.json["code"] == 200

    def test_send_email_not_valid_body(self):
        # Act
        response = self.client.post('/mail/send', json={
            "name": "Test not valid body",
            "phone": "7289293904",
            "message": "Test not valid body email"})
        # Assert
        assert response.json["code"] == 400

    def test_send_email_raise_exception(self):
        self.email_service_mock.send_message.side_effect = EmailInternalErrorException("Error")
        response = self.client.post('/mail/send', json={
            "name": "Test exception",
            "email": "test-exception@test.com",
            "phone": "4728229291",
            "message": "Test exception email"})
        assert response.json["code"] == 500
