# Battery System Simulation Assessment

This assessment focuses on simulating a simplified battery system connected to a solar panel and a load. The goal is to develop a testable simulation and demonstrate understanding of pytest fixtures, generator functions, and basic battery system principles.

## Scenario Description

The system consists of:

* A solar panel that generates power.
* A battery that stores energy.
* A load that consumes energy.

The system's behavior is simulated based on the following components and their interactions:

**System Dynamics:**

1.  **Energy Flow:** Energy flows from the solar panel to the load and/or the battery.
2.  **Charging/Discharging:** The battery charges when the solar panel output exceeds the load consumption and discharges when the load consumption exceeds the solar panel output.
3.  **Selling/Buying:** The grid is used to sell when the solar panel output exceeds the load consumption and the battery is full, and to buy when the load consumption exceeds the solar panel output and the battery is empty.
4.  **Stop working:** The battery stops to work when  the solar panel output equals the load consumption and when battery temperature is not within operational temperature range

## Code Structure

* `utils.py`: Contains all utility functions, Fibonacci generator, read yaml, dump yaml, and setup logging
* `BMS_simulator.py`: Contains the battery system simulation code, the DUT class, and the Controller class
* `tests.py`: contains simulation tests, pytest fixture, and testcases
* `readings.yaml`: to setup the initial configurations and readings

## How to Run the Tests

1.  Create virtual environment: `python -m venv venv`
2.  Install pip requirements: `pip install -r requirements.txt`
3.  Navigate to the directory containing `tests.py`
3.  Run the tests: `pytest tests.py -s -p no:logging`

## Notes

* The simulation is a simplified representation of a real battery system.
* The code can be extended to incorporate more complex models and features.
* The system creates Logs and Output directories during setup if they do not exist.
* The system logs steps in Logs directory.
* The system generate final paramenters report after each TC in Output directory.