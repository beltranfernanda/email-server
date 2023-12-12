import json
import os
from typing import Any


class Config:

    def __init__(self, app):
        self.app = app

    def _get_json_config(self) -> Any:
        config_path = os.path.join(self.app.root_path, "config/config.json")
        with open(config_path) as config_file:
            config_data = json.load(config_file)
        return config_data

    def load_app_config(self) -> None:
        config_data = self._get_json_config()
        for key, config_option in config_data.items():
            environment_variable = config_option["environment_variable"]
            default_value = config_option.get("default")
            self.app.config[key] = os.environ.get(environment_variable, default_value)

    def get_param(self, param: str) -> str:
        return self.app.config[param]
