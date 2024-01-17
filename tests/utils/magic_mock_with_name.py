from unittest.mock import MagicMock


class MagicMockWithName(MagicMock):
    __name__ = "My magic mock test"
