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

    # Test new methods
    data.s_parameters[0, 1, 0] = complex(0.5, 0.0)  # S21 = 0.5 -> IL = 6.02 dB

    assert data.to_return_loss()[0] == pytest.approx(-3.01, 0.01)
    assert data.to_insertion_loss()[0] == pytest.approx(6.02, 0.01)

    # VSWR for S11 = sqrt(2) is not physical (mag > 1), let's set S11 to something < 1
    data.s_parameters[0, 0, 0] = complex(
        0.5, 0.0
    )  # S11 = 0.5 -> VSWR = (1+0.5)/(1-0.5) = 1.5/0.5 = 3
    assert data.to_vswr()[0] == pytest.approx(3.0, 0.01)


def test_in_frequency_range():
    freqs = np.array([1e9, 2e9, 3e9, 4e9])
    s = np.zeros((4, 1, 1), dtype=complex)
    data = TouchstoneData(frequency=freqs, s_parameters=s)

    filtered = data.in_frequency_range(1.5e9, 3.5e9)
    assert filtered.n_freq == 2
    assert filtered.frequency[0] == 2e9
    assert filtered.frequency[1] == 3e9
