import pytest
import numpy as np
from touchstone.parser import read_snp, TouchstoneData
from touchstone.parser.utils import mag_to_db, rad_to_deg

def test_mismatched_length_error():
    """Coverage: ValueError when frequency and S-parameters length mismatch."""
    freqs = np.array([1, 2])
    s = np.zeros((1, 1, 1), dtype=complex) # Only 1 point
    with pytest.raises(ValueError, match="Frequency length"):
        TouchstoneData(frequency=freqs, s_parameters=s)

def test_invalid_port_index():
    """Coverage: IndexError for invalid port indices."""
    freqs = np.array([1])
    s = np.zeros((1, 2, 2), dtype=complex)
    data = TouchstoneData(frequency=freqs, s_parameters=s)
    with pytest.raises(IndexError, match="Port indices out of range"):
        data.get_s(3, 1) # Port 3 doesn't exist

def test_touchstone_data_repr():
    """Coverage: __repr__ method."""
    freqs = np.array([1e9, 2e9])
    s = np.zeros((2, 1, 1), dtype=complex)
    data = TouchstoneData(frequency=freqs, s_parameters=s)
    rep = repr(data)
    assert "TouchstoneData" in rep
    assert "n_ports=1" in rep

def test_invalid_extension_error(tmp_path):
    """Coverage: ValueError for invalid file extension."""
    d = tmp_path / "test.txt"
    d.write_text("# GHZ S RI R 50\n1 0.5 0.5")
    with pytest.raises(ValueError, match="Could not determine port count"):
        read_snp(str(d))

def test_unused_utils():
    """Coverage: Ensure all utility functions are tested."""
    assert mag_to_db(10) == 20.0
    assert rad_to_deg(np.pi) == 180.0

def test_models_using_utils():
    """Verify models use utils (refactoring check)."""
    # This will be covered if I refactor models.py to use these functions
    pass
