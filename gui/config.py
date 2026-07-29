import json
import os


class ConfigMixin:

    CONFIG_FILE = "config.json"

    def load_config(self):

        if not os.path.exists(self.CONFIG_FILE):
            return {}

        with open(self.CONFIG_FILE, "r") as file:
            return json.load(file)


    def save_config(self, config):

        with open(self.CONFIG_FILE, "w") as file:
            json.dump(config, file, indent=4)