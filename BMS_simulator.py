import utils


readings_file = "readings.yaml"


class DUT:
    def __init__(self):
        self.parameters = {}
        self.parameters = utils.read_yaml(readings_file)

    def set(self, key: str, value) -> bool:
        self.parameters[key] = value
        return True

    def get(self, key: str) -> str:
        return self.parameters.get(key, None)


def simulate_SB():
    pass
