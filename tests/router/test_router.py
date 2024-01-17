import unittest
from unittest.mock import patch, MagicMock

from flask import Flask

from app.router.router import map_routes
from tests.utils.magic_mock_with_name import MagicMockWithName


class TestRouter(unittest.TestCase):
    @patch("app.router.router.load_dependencies")
    def test_map_routes(self, mock_load_dependencies):
        # Arrange
        app = MagicMock(spec=Flask)

        mock_instances = {"ping": MagicMockWithName(), "email": MagicMockWithName()}
        mock_load_dependencies.return_value = mock_instances

        # Act
        map_routes(app)

        # Assert
        mock_load_dependencies.assert_called_once_with(app)
