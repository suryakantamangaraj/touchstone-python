import pytest
import numpy as np
from touchstone.parser import read_snp

def test_ri_conversion_accuracy(tmp_path):
    """Numerical: Real/Imaginary to Complex."""
    d = tmp_path / "test.s1p"
    d.write_text("# GHZ S RI R 50\n1.0 0.123456789 0.987654321")
    data = read_snp(str(d))
    assert data.s_parameters[0, 0, 0] == complex(0.123456789, 0.987654321)

def test_ma_conversion_accuracy(tmp_path):
    """Numerical: Magnitude/Angle to Complex."""
    d = tmp_path / "test.s1p"
    # Mag=1, Angle=45 deg -> 0.707 + 0.707j
    d.write_text("# GHZ S MA R 50\n1.0 1.0 45.0")
    data = read_snp(str(d))
    expected = 1.0 * (np.cos(np.pi/4) + 1j * np.sin(np.pi/4))
    assert np.allclose(data.s_parameters[0, 0, 0], expected)

def test_db_conversion_accuracy(tmp_path):
    """Numerical: dB/Angle to Complex."""
    d = tmp_path / "test.s1p"
    # -20dB, 180 deg -> Mag=0.1, Phase=180 -> -0.1 + 0j
    d.write_text("# GHZ S DB R 50\n1.0 -20.0 180.0")
    data = read_snp(str(d))
    assert np.allclose(data.s_parameters[0, 0, 0], -0.1 + 0j)

def test_helper_method_precision():
    """Numerical: magnitude() and phase() accuracy."""
    from touchstone.parser.models import TouchstoneData
    freqs = np.array([1e9])
    s = np.zeros((1, 1, 1), dtype=complex)
    s[0, 0, 0] = 0.5 + 0.5j
    data = TouchstoneData(frequency=freqs, s_parameters=s)
    
    # Mag = sqrt(0.5^2 + 0.5^2) = sqrt(0.5) approx 0.7071
    assert np.allclose(data.magnitude(1, 1, db=False), np.sqrt(0.5))
    # Phase = 45 deg
    assert np.allclose(data.phase(1, 1, deg=True), 45.0)
