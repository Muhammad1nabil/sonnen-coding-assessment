import utils
import logging


readings_file = "readings.yaml"


class Controller:

    def __init__(self, inputs):
        # setting Controller variables
        self.inputs = inputs
        self.command = ""
        self.grid_total = 0
        self.inverter_power = 0
        self.inverter_voltage = 0
        self.inverter_frequency = 0
        self.capacity_percentage = 0

    def calculate_capacity_percentage(self):
        self.capacity_percentage = self.inputs["storage_capacity"] / (
            self.inputs["usable_capacity"] * self.inputs["BMS_count"]
        )
        logging.info(f"storage capacity {self.capacity_percentage}%")

    def temp_safty_check(self):
        """
        temperature safty check to only operate within operational temperature
        and flag with the battery is outside operational range
        also it flags if the temperature within best condition range
        :Return:
            - True: if the temperature operational
            - False: if temperature outside operational range
        """

        if (
            self.inputs["operational_temp"][0]
            < self.inputs["BMS_temp"]
            < self.inputs["operational_temp"][1]
        ):
            if (
                self.inputs["best_condition_temp"][0]
                < self.inputs["BMS_temp"]
                < self.inputs["best_condition_temp"][1]
            ):
                logging.info(
                    f"Battery in best condition temperature. ({self.inputs['BMS_temp']} C)"
                )
            return True
        else:
            logging.critical(
                f"Battery is switching off. battery temperature is not in operational temperature range "
                + f"(min {self.inputs['operational_temp'][0]} max {self.inputs['operational_temp'][1]})"
            )
            return False

    def execute_charge_battery(self):
        """
        execute charge battery steps
        """
        self.command = "Charge - Battery"
        # output limited by inverter and battery max power
        # considering inverter power sign to be (+) in case charging
        self.inverter_power = min(
            self.inputs["pv_panel_power"] - self.inputs["load_power"],
            self.inputs["inverter_max_power"],
            self.inputs["BMS_max_power"],
        )

        msg = (
            f"charging battery with (PV production ({self.inputs['pv_panel_power']})"
            + f" - load consumption ({self.inputs['load_power']})) by rate ({self.inverter_power})"
        )
        logging.info(msg)

    def execute_sell_grid(self):
        """
        execute sell grid steps
        """

        self.command = "Sell - Grid"

        # reflecting the surplus production in grid_power_total with (+)
        self.grid_total += self.inputs["pv_panel_power"] - self.inputs["load_power"]

        # not sure if the following 2 lines wont blow up the building or not tbh xD
        self.output_frequency = self.inputs["inverter_grid_frequency"]
        self.output_voltage = self.inputs["inverter_grid_voltage"]

        msg = f"selling PV production surplus ({self.inputs['pv_panel_power'] - self.inputs['load_power']} W) to the grid"

        logging.info(msg)

    def execute_discharge_battery(self):
        """
        execute discharge battery steps
        """

        self.command = "Discharge - Battery"
        # discharging with a limitation of inverter max power and BMS max power
        # considering inverter power sign to be (-) in case discharging
        self.inverter_power = -min(
            self.inputs["load_power"] - self.inputs["pv_panel_power"],
            self.inputs["inverter_max_power"],
            self.inputs["BMS_max_power"],
        )

        self.output_frequency = self.inputs["load_frequency"]
        self.output_voltage = self.inputs["load_voltage"]

        # deduct the consumed power provided from battery from battery capacity

        msg = (
            f"discharging battery to provide the difference "
            + f"(load consumption ({self.inputs['load_power']} W) - "
            + f"PV production ({self.inputs['pv_panel_power']} W))"
        )
        logging.info(msg)

    def execute_buy_grid(self):
        """
        execute buy grid steps
        """
        self.command = "Buy - Grid"
        # reflecting the consumption gap in grid_power_total with (-)
        self.grid_total -= self.inputs["load_power"] - self.inputs["pv_panel_power"]

        msg = (
            f"buying PV production deficiency ({self.inputs['load_power'] - self.inputs['pv_panel_power']} W)"
            + f" from the grid"
        )
        logging.info(msg)

    def execute_none_battery(self):
        """
        execute none battery steps
        """
        self.command = "None - Battery"
        logging.info("PV production is equal to load consumption. no SB action needed")

    def execute_temp_check_fail(self):
        """
        execute none battery steps with critical log for safty check fail
        """
        self.command = "None - Battery"
        logging.critical("energy flow is off.")

    def energy_flow(self):
        """
        function to decide what flow SB execute for the energy where commands can only be:
            command structure (action - entity) or no command
            - Charge - Battery
            - Discharge - Battery
            - Sell - Grid
            - Buy - Grid
            - None - Battery
        :return:
            - command: based on energy flow algorithm
        """

        # safty check before execution
        if not self.temp_safty_check():
            self.execute_temp_check_fail()
            return self.command

        # calculate SB capacity percentage
        self.calculate_capacity_percentage()

        # case: over production
        if self.inputs["pv_panel_power"] > self.inputs["load_power"]:
            # case: over production and battery is not full
            if self.capacity_percentage < 1:
                self.execute_charge_battery()

            # case: over production and battery is full
            elif self.capacity_percentage == 1:
                self.execute_sell_grid()

        # case: production deficiency
        elif self.inputs["pv_panel_power"] < self.inputs["load_power"]:
            # case: production deficiency and buttery is not empty
            if self.capacity_percentage > 0:
                self.execute_discharge_battery()

            # case: production deficiency and buttery is empty
            elif self.capacity_percentage == 0:
                self.execute_buy_grid()
        # case: production equal consumption
        else:
            self.execute_none_battery()

        return self.command


class DUT:
    def __init__(self):
        self.parameters = {}
        self.parameters = utils.read_yaml(readings_file)
        self.controller = Controller(self.parameters)

    def set(self, key: str, value) -> bool:
        self.parameters[key] = value
        return True

    def get(self, key: str) -> str:
        return self.parameters.get(key, None)
