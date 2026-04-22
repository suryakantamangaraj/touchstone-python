import numpy as np
import pytest
from touchstone.parser import TouchstoneData
from touchstone.parser.utilities.touchstone_data_extensions import (
    get_magnitude,
    get_phase,
)


def test_touchstone_data_extensions():
    freqs = np.array([1e9])
    s = np.zeros((1, 2, 2), dtype=complex)
    s[0, 0, 0] = complex(1.0, 1.0)
    data = TouchstoneData(frequency=freqs, s_parameters=s)

    mag_db = get_magnitude(data, 1, 1, db=True)
    phase_deg = get_phase(data, 1, 1, deg=True)

    # 1+1j => abs = sqrt(2) => db = 20 * log10(sqrt(2)) = ~3.01 dB
    # angle = 45 degrees
    assert mag_db[0] == pytest.approx(3.01, 0.01)
    assert phase_deg[0] == pytest.approx(45.0, 0.01)
