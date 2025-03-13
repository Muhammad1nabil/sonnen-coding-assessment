import pytest
from utils import fibonacci_generator
from BMS_simulator import DUT, simulate_SB

@pytest.fixture
def dut():
    dut = DUT()


    """
    Tests the battery simulation using Fibonacci generators to populate
    solar panel and load readings.
    """
    # Initialize Fibonacci generators
    solar_voltage_gen = fibonacci_generator()
    solar_current_gen = fibonacci_generator()
    load_current_gen = fibonacci_generator()

    # Initial battery state
    battery_voltage = 12.0
    battery_capacity = 10.0
    battery_charge = 5.0

    # Simulate for a few steps
    for _ in range(5):
        # Mock DUT readings using Fibonacci values
        solar_panel_voltage = next(solar_voltage_gen) % 20  # Example range
        solar_panel_current = next(solar_current_gen) % 6    # Example range
        load_current = next(load_current_gen) % 4           # Example range

        dut.set("solar_panel_voltage", solar_panel_voltage)
        dut.set("solar_panel_current", solar_panel_current)
        dut.set("load_current", load_current)
        dut.set("battery_voltage", battery_voltage)
        dut.set("battery_capacity", battery_capacity)
        dut.set("battery_charge", battery_charge)

        # Run the simulation
        battery_voltage = float(dut.get("battery_voltage"))
        battery_capacity = float(dut.get("battery_capacity"))
        battery_charge = float(dut.get("battery_charge"))

        battery_voltage, battery_current, battery_charge = simulate_battery_system(
            solar_panel_voltage, solar_panel_current, load_current,
            battery_voltage, battery_capacity, battery_charge
        )

        # Update DUT state with the results
        dut.set("battery_voltage", battery_voltage)
        dut.set("battery_current", battery_current)
        dut.set("battery_charge", battery_charge)

        # Assertions (Example: Check if charge is within bounds)
        assert 0 <= float(dut.get("battery_charge")) <= battery_capacity
        assert 10 <= float(dut.get("battery_voltage")) <= 15
        # Add more specific assertions based on expected behavior