import numpy as np
import pytest

from touchstone.parser import TouchstoneData, TouchstoneOptions


def test_stress():
    # Simulate a large file
    n_freq = 1000
    n_ports = 10
    freqs = np.linspace(1e9, 10e9, n_freq)
    s_params = np.random.rand(n_freq, n_ports, n_ports) + 1j * np.random.rand(
        n_freq, n_ports, n_ports
    )

    data = TouchstoneData(frequency=freqs, s_parameters=s_params)
    assert data.n_ports == 10
    assert data.n_freq == 1000
    assert data.s_parameters.shape == (1000, 10, 10)
