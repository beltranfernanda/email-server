import unittest
from unittest.mock import patch, Mock

from flask import Flask

from app.router.router import map_routes


class TestRouter(unittest.TestCase):

    @patch('app.router.router.load_dependencies')
    def test_map_routes(self, mock_load_dependencies):
        # Arrange
        app = Mock(spec=Flask)

        mock_instances = {
            'ping': Mock(),
            'email': Mock()
        }
        mock_load_dependencies.return_value = mock_instances

        # Act
        map_routes(app)

        # Assert
        app.add_url_rule.assert_any_call("/ping", view_func=mock_instances['ping'].ping)
        app.add_url_rule.assert_any_call("/mail/send", view_func=mock_instances['email'].send_mail, methods=['POST'])
        mock_load_dependencies.assert_called_once_with(app)
