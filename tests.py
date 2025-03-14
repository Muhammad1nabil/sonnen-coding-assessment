import pytest
import utils
from BMS_simulator import DUT
import logging
from datetime import datetime


@pytest.fixture
def dut():
    # setup
    utils.setup_logging()
    dut = DUT()
    initial_state = dut.parameters.copy()
    yield dut

    # teardown
    
    dut.parameters = initial_state


@pytest.mark.parametrize(
    "TC, pv_panel_power, load_power, storage_capacity, BMS_temp, inverter_power, command",
    [
        # Test Case 1: over production, charge battery
        (1, 1000, 500, 8000, 15, 500, "Charge - Battery"),
        # Test Case 2: over production and battery is full, sell to grid
        (2, 1000, 500, 10000, 15, 0, "Sell - Grid"),
        # Test Case 3: production deficiency, discharge battery
        (3, 500, 1000, 8000, 15, -500, "Discharge - Battery"),
        # Test Case 4: production deficiency and battery is empty, buy from grid
        (4, 500, 1000, 0, 15, 0, "Buy - Grid"),
        # Test Case 5: over production, charge battery, max charge limit
        (5, 2000, 500, 8000, 15, 1000, "Charge - Battery"),
        # Test Case 6: production deficiency, discharge battery, max discharge limit
        (6, 500, 2000, 8000, 15, -1000, "Discharge - Battery"),
        # Test Case 7: battery temperature is less than min
        (7, 1000, 500, 8000, -15, 0, "None - Battery"),
        # Test Case 8: battery temperature is more than max
        (8, 1000, 500, 8000, 55, 0, "None - Battery"),
    ],
)
def test_energy_algorithm(
    dut,
    TC,
    pv_panel_power,
    load_power,
    storage_capacity,
    BMS_temp,
    inverter_power,
    command
):
    dut.set("pv_panel_power", pv_panel_power)
    dut.set("load_power", load_power)
    dut.set("storage_capacity", storage_capacity)
    dut.set("BMS_temp", BMS_temp)

    result = dut.controller.energy_flow()

    assert command == result
    assert dut.controller.inverter_power == inverter_power
    dut.set("grid_total", dut.controller.grid_total)
    dut.set("inverter_power", dut.controller.inverter_power)
    dut.set("inverter_voltage", dut.controller.inverter_voltage)
    dut.set("inverter_frequency", dut.controller.inverter_frequency)
    dut.set("capacity_percentage", dut.controller.capacity_percentage)
    dut.set("command", dut.controller.command)
    utils.dump_yaml(
        dut.parameters,
        utils.output_folder.joinpath(f"TC {TC}_run_final_parameters.yaml"),
    )
