import unittest
from unittest.mock import patch

from flask import Flask
from app.router.dependencies import load_dependencies


class TestDependencies(unittest.TestCase):
    @patch("app.router.dependencies.PingController")
    @patch("app.router.dependencies.Config")
    @patch("app.router.dependencies.EmailService")
    @patch("app.router.dependencies.EmailController")
    def test_load_dependencies(
        self,
        mock_email_controller,
        mock_email_service,
        mock_config,
        mock_ping_controller,
    ):
        # Arrange
        app = Flask(__name__)

        # Act
        result = load_dependencies(app)

        # Assert
        self.assertIn("ping", result)
        self.assertEqual(result["ping"], mock_ping_controller.return_value)

        self.assertIn("email", result)
        self.assertEqual(result["email"], mock_email_controller.return_value)
