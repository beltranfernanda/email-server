import smtplib
import unittest
from unittest.mock import MagicMock, mock_open, patch

from app.exception.email_internal_error_exception import EmailInternalErrorException
from app.service.mail import EmailService


class TestMailService(unittest.TestCase):
    def setUp(self):
        self.config_mock = MagicMock()
        self.email_service = EmailService(self.config_mock)

    @patch("smtplib.SMTP")
    @patch("builtins.open", new_callable=mock_open, read_data="dummy html content")
    def test_send_message(self, mock_file, mock_smtp):
        # Arrange
        self.config_mock.get_param.side_effect = [
            "smtp.server.com",
            "587",
            "test@test.com",
            "test@test.com",
            "test",
            "test",
            "test@test.com",
            "test@test.com",
        ]
        mock_server = mock_smtp.return_value.__enter__.return_value

        # Act
        self.email_service.send_message("Test", "test@test.com", "123", "Test message")

        # Assert
        mock_server.sendmail.assert_called_once()
        mock_server.login.assert_called_with("test", "test")
        mock_file.assert_called_once()
        self.assertEqual(mock_server.sendmail.call_args[0][0], "test@test.com")
        self.assertEqual(mock_server.sendmail.call_args[0][1], "test@test.com")

    @patch("smtplib.SMTP")
    def test_send_message_exception(self, mock_smtp):
        # Arrange
        self.config_mock.get_param.side_effect = [
            "smtp.server.com",
            "587",
            "test@test.com",
            "test@test.com",
            "test",
            "test",
            "test@test.com",
            "test@test.com",
        ]
        mock_smtp.side_effect = smtplib.SMTPException

        # Act & Assert
        with self.assertRaises(EmailInternalErrorException):
            self.email_service.send_message(
                "Test ex", "test@testexp.com", "456", "Test exception"
            )
