import pytest
import utils
from BMS_simulator import DUT, simulate_SB
import logging


@pytest.fixture
def fixture_dut():
    # setup
    utils.setup_logging()
    dut = DUT()
    initial_state = dut.parameters.copy()
    yield dut

    # teardown
    utils.dump_yaml(
        dut.parameters, utils.output_folder.joinpath("run_final_parameters.yaml")
    )
    dut.parameters = initial_state


def test(fixture_dut):
    pass
