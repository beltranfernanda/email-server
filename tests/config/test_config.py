import unittest

from unittest.mock import patch, MagicMock
from app.config.config import Config


class TestConfig(unittest.TestCase):
    def setUp(self):
        self.app = MagicMock()
        self.app.root_path = "/app"
        self.config = Config(self.app)

    @patch("json.load")
    @patch("builtins.open")
    def test_get_json_config(self, mock_open, mock_load):
        # Arrange
        file_content = {
            "test-param": {"environment_variable": "VALUE1", "default": "default"}
        }
        mock_load.return_value = file_content

        # Act
        result = self.config._get_json_config()

        # Assert
        mock_open.assert_called_once_with("/app/config/config.json")
        mock_load.assert_called_once_with(mock_open().__enter__())
        self.assertEqual(result, file_content)

    @patch.object(Config, "_get_json_config")
    def test_load_app_config(self, mock_get_json_config):
        # Arrange
        self.app.config = {}
        mock_get_json_config.return_value = {
            "test-param": {"environment_variable": "VALUE1", "default": "default"}
        }

        # Act
        self.config.load_app_config()

        # Assert
        mock_get_json_config.assert_called_once()
        self.assertEqual(self.app.config, {"test-param": "default"})

    def test_get_param(self):
        # Arrange
        self.app.config = {"param1": "value1", "param2": "value2"}

        # Act
        result = self.config.get_param("param1")

        # Assert
        self.assertEqual(result, "value1")
