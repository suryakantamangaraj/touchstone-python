"""Tests for TouchstoneData extension methods and RF calculations."""

import numpy as np
import numpy.testing as npt
import pytest

from touchstone.parser import TouchstoneData
from touchstone.parser.utilities.touchstone_data_extensions import (
    get_magnitude,
    get_phase,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_data(s11=0 + 0j, s21=0 + 0j, s12=0 + 0j, s22=0 + 0j, n_ports=2):
    """Create a single-frequency TouchstoneData with given S-parameters."""
    freqs = np.array([1e9])
    s = np.zeros((1, n_ports, n_ports), dtype=complex)
    if n_ports >= 1:
        s[0, 0, 0] = s11
    if n_ports >= 2:
        s[0, 1, 0] = s21
        s[0, 0, 1] = s12
        s[0, 1, 1] = s22
    return TouchstoneData(frequency=freqs, s_parameters=s)


# ---------------------------------------------------------------------------
# get_magnitude / get_phase
# ---------------------------------------------------------------------------


class TestMagnitudeAndPhase:
    """Tests for get_magnitude and get_phase helpers."""

    def test_magnitude_db_known_value(self):
        """1+1j => |z| = sqrt(2) => 20*log10(sqrt(2)) ≈ 3.0103 dB."""
        data = _make_data(s11=complex(1.0, 1.0))
        mag_db = get_magnitude(data, 1, 1, db=True)
        npt.assert_allclose(mag_db, [3.0103], atol=1e-4)

    def test_magnitude_linear_known_value(self):
        """1+1j => |z| = sqrt(2) ≈ 1.41421."""
        data = _make_data(s11=complex(1.0, 1.0))
        mag_lin = get_magnitude(data, 1, 1, db=False)
        npt.assert_allclose(mag_lin, [np.sqrt(2)], atol=1e-10)

    def test_phase_degrees_known_value(self):
        """1+1j => angle = 45°."""
        data = _make_data(s11=complex(1.0, 1.0))
        phase_deg = get_phase(data, 1, 1, deg=True)
        npt.assert_allclose(phase_deg, [45.0], atol=1e-10)

    def test_phase_radians_known_value(self):
        """1+1j => angle = pi/4 rad."""
        data = _make_data(s11=complex(1.0, 1.0))
        phase_rad = get_phase(data, 1, 1, deg=False)
        npt.assert_allclose(phase_rad, [np.pi / 4], atol=1e-10)


# ---------------------------------------------------------------------------
# Return Loss
# ---------------------------------------------------------------------------


class TestReturnLoss:
    """Tests for to_return_loss."""

    @pytest.mark.parametrize(
        "s11, expected_rl",
        [
            # |S11| = 0.5 => RL = -20*log10(0.5) = 6.0206 dB
            (complex(0.5, 0.0), 6.0206),
            # |S11| = 0.1 => RL = -20*log10(0.1) = 20.0 dB
            (complex(0.1, 0.0), 20.0),
            # |S11| = 0.316228 => RL ≈ 10.0 dB
            (complex(0.316228, 0.0), 10.0),
        ],
        ids=["rl_6dB", "rl_20dB", "rl_10dB"],
    )
    def test_return_loss_parametrized(self, s11, expected_rl):
        data = _make_data(s11=s11)
        rl = data.to_return_loss()
        npt.assert_allclose(rl, [expected_rl], atol=1e-2)


# ---------------------------------------------------------------------------
# Insertion Loss
# ---------------------------------------------------------------------------


class TestInsertionLoss:
    """Tests for to_insertion_loss."""

    @pytest.mark.parametrize(
        "s21, expected_il",
        [
            # |S21| = 0.5 => IL = -20*log10(0.5) = 6.0206 dB
            (complex(0.5, 0.0), 6.0206),
            # |S21| = 1.0 => IL = 0 dB (lossless)
            (complex(1.0, 0.0), 0.0),
            # |S21| = 0.1 => IL = 20.0 dB
            (complex(0.1, 0.0), 20.0),
        ],
        ids=["il_6dB", "il_lossless", "il_20dB"],
    )
    def test_insertion_loss_parametrized(self, s21, expected_il):
        data = _make_data(s21=s21)
        il = data.to_insertion_loss()
        npt.assert_allclose(il, [expected_il], atol=1e-2)

    def test_insertion_loss_requires_two_ports(self):
        """Insertion loss should raise ValueError for 1-port data."""
        freqs = np.array([1e9])
        s = np.zeros((1, 1, 1), dtype=complex)
        data = TouchstoneData(frequency=freqs, s_parameters=s)
        with pytest.raises(ValueError, match="at least 2 ports"):
            data.to_insertion_loss()


# ---------------------------------------------------------------------------
# VSWR
# ---------------------------------------------------------------------------


class TestVSWR:
    """Tests for to_vswr."""

    @pytest.mark.parametrize(
        "s11, expected_vswr",
        [
            # |S11| = 0.5 => VSWR = (1+0.5)/(1-0.5) = 3.0
            (complex(0.5, 0.0), 3.0),
            # |S11| = 0.0 => VSWR = 1.0 (perfectly matched)
            (complex(0.0, 0.0), 1.0),
            # |S11| = 0.333 => VSWR ≈ (1.333)/(0.667) ≈ 1.998
            (complex(0.333, 0.0), 1.998),
            # Complex S11: |0.3+0.4j| = 0.5 => VSWR = 3.0
            (complex(0.3, 0.4), 3.0),
        ],
        ids=["vswr_3", "vswr_perfect", "vswr_2", "vswr_complex"],
    )
    def test_vswr_parametrized(self, s11, expected_vswr):
        data = _make_data(s11=s11)
        vswr = data.to_vswr()
        npt.assert_allclose(vswr, [expected_vswr], atol=1e-2)


# ---------------------------------------------------------------------------
# Frequency Range Filtering
# ---------------------------------------------------------------------------


class TestFrequencyRange:
    """Tests for in_frequency_range."""

    def test_basic_filtering(self):
        freqs = np.array([1e9, 2e9, 3e9, 4e9])
        s = np.zeros((4, 1, 1), dtype=complex)
        data = TouchstoneData(frequency=freqs, s_parameters=s)

        filtered = data.in_frequency_range(1.5e9, 3.5e9)
        assert filtered.n_freq == 2
        npt.assert_array_equal(filtered.frequency, [2e9, 3e9])

    def test_inclusive_bounds(self):
        """Boundaries are inclusive."""
        freqs = np.array([1e9, 2e9, 3e9])
        s = np.zeros((3, 1, 1), dtype=complex)
        data = TouchstoneData(frequency=freqs, s_parameters=s)

        filtered = data.in_frequency_range(1e9, 3e9)
        assert filtered.n_freq == 3

    def test_empty_result(self):
        """Filtering outside the range returns empty data."""
        freqs = np.array([1e9, 2e9])
        s = np.zeros((2, 1, 1), dtype=complex)
        data = TouchstoneData(frequency=freqs, s_parameters=s)

        filtered = data.in_frequency_range(5e9, 6e9)
        assert filtered.n_freq == 0

    def test_preserves_s_parameters(self):
        """Ensure S-parameter values survive filtering correctly."""
        freqs = np.array([1e9, 2e9, 3e9])
        s = np.zeros((3, 2, 2), dtype=complex)
        s[1, 0, 0] = complex(0.5, 0.3)  # at 2 GHz
        data = TouchstoneData(frequency=freqs, s_parameters=s)

        filtered = data.in_frequency_range(1.5e9, 2.5e9)
        assert filtered.n_freq == 1
        npt.assert_equal(filtered.s_parameters[0, 0, 0], complex(0.5, 0.3))
