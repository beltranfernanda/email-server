import unittest

from app.exception.env_variable_not_found_exception import EnvVariableNotFoundException


class TestEmailInternalErrorException(unittest.TestCase):

    def test_default_message(self):
        exception = EnvVariableNotFoundException()
        self.assertEqual(str(exception), "Environment variable value not found")

    def test_custom_message(self):
        custom_message = "Test error message"
        exception = EnvVariableNotFoundException(custom_message)
        self.assertEqual(str(exception), custom_message)
