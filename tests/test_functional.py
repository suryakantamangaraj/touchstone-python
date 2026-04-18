import numpy as np
import pytest

from touchstone.parser import read_snp


def test_parse_s1p_basic(tmp_path):
    """Functional: Basic 1-port parsing."""
    d = tmp_path / "test.s1p"
    d.write_text("# MHZ S RI R 50\n100 0.5 0.5")
    data = read_snp(str(d))
    assert data.n_ports == 1
    assert data.s_parameters[0, 0, 0] == complex(0.5, 0.5)


def test_parse_s2p_matrix_ordering(tmp_path):
    """Functional: Verify S21/S12 special ordering for 2-port files."""
    d = tmp_path / "test.s2p"
    # Format: freq s11 s21 s12 s22
    d.write_text("# GHZ S RI R 50\n1.0 1.1 1.1 2.1 2.1 1.2 1.2 2.2 2.2")
    data = read_snp(str(d))
    # S21 should be (2.1, 2.1)
    assert data.s_parameters[0, 1, 0] == complex(2.1, 2.1)
    # S12 should be (1.2, 1.2)
    assert data.s_parameters[0, 0, 1] == complex(1.2, 1.2)


def test_parse_snp_matrix_ordering(tmp_path):
    """Functional: Verify row-major ordering for N > 2."""
    d = tmp_path / "test.s3p"
    # Row 1: S11, S12, S13
    # Row 2: S21, S22, S23
    # Row 3: S31, S32, S33
    d.write_text("""# GHZ S RI R 50
1 1.1 1.1 1.2 1.2 1.3 1.3
  2.1 2.1 2.2 2.2 2.3 2.3
  3.1 3.1 3.2 3.2 3.3 3.3""")
    data = read_snp(str(d))
    assert data.n_ports == 3
    assert data.s_parameters[0, 0, 2] == complex(1.3, 1.3)  # S13
    assert data.s_parameters[0, 2, 0] == complex(3.1, 3.1)  # S31
