import os
from touchstone.parser import TouchstoneParser

TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), "test_data")


def test_multi_port():
    filepath = os.path.join(TEST_DATA_DIR, "filter_4port.s4p")
    data = TouchstoneParser.parse(filepath)
    assert data.n_ports == 4
    assert data.s_parameters.shape[1] == 4
    assert data.s_parameters.shape[2] == 4
