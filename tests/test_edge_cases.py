import pytest
import numpy as np
from touchstone.parser import read_snp

def test_mixed_delimiters_robustness(tmp_path):
    """Edge: Mixed spaces, tabs, and commas."""
    d = tmp_path / "test.s1p"
    d.write_text("# GHZ S RI R 50\n1.0, 0.5\t0.5\n2.0,0.6 , 0.6")
    data = read_snp(str(d))
    assert len(data.frequency) == 2
    assert data.s_parameters[1, 0, 0] == complex(0.6, 0.6)

def test_abrupt_eof_handling(tmp_path):
    """Edge: File ends mid-block."""
    d = tmp_path / "test.s2p"
    # Needs 9 numbers. We give 9 for first point, then 2 for second point.
    d.write_text("# GHZ S RI R 50\n1 0 0 0 0 0 0 0 0\n2 0")
    data = read_snp(str(d))
    assert len(data.frequency) == 1

def test_non_numeric_noise_in_data(tmp_path):
    """Edge: Skip non-numeric data entries."""
    d = tmp_path / "test.s1p"
    d.write_text("# GHZ S RI R 50\n1.0 0.5 0.5\nINVALID 0.6 0.6\n3.0 0.7 0.7")
    data = read_snp(str(d))
    # 1.0 0.5 0.5 (3)
    # 0.6 0.6 3.0 (3)
    # 0.7 0.7 (2) -> truncated
    assert len(data.frequency) == 2

def test_extra_lines_and_whitespace(tmp_path):
    """Edge: Multiple empty lines and leading/trailing spaces."""
    d = tmp_path / "test.s1p"
    d.write_text("\n\n  # GHZ S RI R 50  \n\n  1.0  0.5  0.5  \n\n")
    data = read_snp(str(d))
    assert len(data.frequency) == 1
    assert data.frequency[0] == 1e9
