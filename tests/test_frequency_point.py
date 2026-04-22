import numpy as np
import pytest

from touchstone.parser.models.frequency_point import FrequencyPoint


def test_frequency_point_valid():
    s_params = np.array([[1 + 0j, 0 + 0j], [0 + 0j, 1 + 0j]], dtype=complex)
    fp = FrequencyPoint(1e9, s_params)
    assert fp.frequency_hz == 1e9
    assert fp.number_of_ports == 2


def test_negative_frequency_throws():
    s_params = np.array([[1 + 0j]], dtype=complex)
    with pytest.raises(ValueError):
        FrequencyPoint(-1.0, s_params)


def test_non_square_matrix_throws():
    s_params = np.array([[1 + 0j, 0 + 0j]], dtype=complex)
    with pytest.raises(ValueError):
        FrequencyPoint(1e9, s_params)


def test_index_out_of_range_throws():
    s_params = np.array([[1 + 0j]], dtype=complex)
    fp = FrequencyPoint(1e9, s_params)
    with pytest.raises(IndexError):
        _ = fp[1, 1]


def test_get_parameter_matrix_is_copy():
    s_params = np.array([[1 + 0j]], dtype=complex)
    fp = FrequencyPoint(1e9, s_params)
    matrix = fp.get_parameter_matrix()
    matrix[0, 0] = 0 + 0j
    assert fp[0, 0].real == 1.0
