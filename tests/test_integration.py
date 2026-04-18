import numpy as np
import pytest

from touchstone.parser import read_snp


def test_numpy_integration(tmp_path):
    """Integration: Verify parsed data works with NumPy operations."""
    d = tmp_path / "test.s2p"
    # Freq=1, S11=0.5+0j, S21=0+0j, S12=0+0j, S22=0.5+0j
    d.write_text("# GHZ S RI R 50\n1 0.5 0 0 0 0 0 0.5 0")
    data = read_snp(str(d))

    # Check if s_parameters is a real numpy array
    assert isinstance(data.s_parameters, np.ndarray)

    # Perform a matrix operation (e.g., determinant)
    s_matrix = data.s_parameters[0]
    det = np.linalg.det(s_matrix)
    # det([0.5 0; 0 0.5]) = 0.25
    assert np.isclose(det, 0.25)


def test_high_level_api_usage(tmp_path):
    """Integration: Verify the main entry point and public API."""
    import touchstone.parser as tp

    d = tmp_path / "test.s1p"
    d.write_text("# GHZ S RI R 50\n1 0.5 0.5")

    data = tp.read_snp(str(d))
    assert data.n_ports == 1
    assert tp.db_to_mag(-20) == 0.1
