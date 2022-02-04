import json


class ForceSetting(object):
    def __init__(self, config_path):
        with open(config_path, 'r', encoding="UTF-8") as f:
            self.cfg = json.load(f)

    @property
    def parameters(self):
        return self.cfg["forces"]["parameters"]

    @property
    def ped_repulsive_force(self):
        return self.parameters["ped_repulsive_force"]

    @property
    def social_force(self):
        return self.parameters["my_force"]
        