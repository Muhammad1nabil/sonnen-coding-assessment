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


def energy_flow(pv_panel_power, load_power, battery_capacity):
    if pv_panel_power > load_power:
        if battery_capacity < 1:
            print("charging battery with (PV production - load consumption)")
        elif battery_capacity == 1:
            print("selling PV production - load power to the grid")
    else:
        if battery_capacity > 0:
            print(
                "discharging battery to provide the difference (load consumption - PV production)"
            )
        elif battery_capacity == 0:
            print(
                "using the grid to provide the difference (load consumption - PV production)"
            )


