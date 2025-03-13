import yaml

class DUT:
    def __init__(self):
        self.parameters = {}
        self.parameters = yaml.load("readings.yaml", 'r')

    def set(self, key: str, value) -> bool:
        self.parameters[key] = value
        return True

    def get(self, key: str) -> str:
        return self.parameters.get(key, None)

def simulate_SB():
    pass
