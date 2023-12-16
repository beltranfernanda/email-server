import unittest

from app.exception.email_internal_error_exception import EmailInternalErrorException


class TestEmailInternalErrorException(unittest.TestCase):

    def test_default_message(self):
        exception = EmailInternalErrorException()
        self.assertEqual(str(exception), "An error has occurred sending message")

    def test_custom_message(self):
        custom_message = "Test error message"
        exception = EmailInternalErrorException(custom_message)
        self.assertEqual(str(exception), custom_message)
