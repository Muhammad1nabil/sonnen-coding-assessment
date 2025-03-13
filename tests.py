import pytest
import utils
from BMS_simulator import DUT, simulate_SB
import logging
from datetime import datetime


@pytest.fixture
def fixture_dut():
    # setup
    utils.setup_logging()
    dut = DUT()
    initial_state = dut.parameters.copy()
    yield dut

    # teardown
    now = datetime.now().strftime("%H%M%S")
    utils.dump_yaml(
        dut.parameters, utils.output_folder.joinpath(f"{now}_run_final_parameters.yaml")
    )
    dut.parameters = initial_state


def test(fixture_dut):
    pass
