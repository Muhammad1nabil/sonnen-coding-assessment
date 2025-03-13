import pytest
import utils
from BMS_simulator import DUT, simulate_SB

@pytest.fixture
def fixture_dut():
    # setup 
    dut = DUT()
    initial_state = dut.parameters.copy()
    yield dut

    # teardown
    dut.parameters = initial_state

def test(fixture_dut):
    pass