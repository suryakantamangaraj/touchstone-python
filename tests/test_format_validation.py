import pytest

from touchstone.parser import read_snp


@pytest.mark.parametrize(
    "unit,multiplier", [("HZ", 1), ("KHZ", 1e3), ("MHZ", 1e6), ("GHZ", 1e9)]
)
def test_unit_normalization(tmp_path, unit, multiplier):
    """Format: Verify frequency unit conversion to Hz."""
    d = tmp_path / "test.s1p"
    d.write_text(f"# {unit} S RI R 50\n1.0 0.5 0.5")
    data = read_snp(str(d))
    assert data.frequency[0] == multiplier


@pytest.mark.parametrize("param", ["S", "Y", "Z", "G", "H"])
def test_parameter_type_detection(tmp_path, param):
    """Format: Verify detection of parameter type."""
    d = tmp_path / "test.s1p"
    d.write_text(f"# GHZ {param} RI R 50\n1.0 0.5 0.5")
    data = read_snp(str(d))
    assert data.parameter == param


def test_reference_resistance_parsing(tmp_path):
    """Format: Verify parsing of reference impedance."""
    d = tmp_path / "test.s1p"
    d.write_text("# GHZ S RI R 75\n1.0 0.5 0.5")
    data = read_snp(str(d))
    assert data.z0 == 75.0


def test_comment_handling_variations(tmp_path):
    """Format: Verify robustness against various comment placements."""
    d = tmp_path / "test.s1p"
    d.write_text("""! Start comment
# GHZ S RI R 50 ! Inline header comment
! Middle comment
1.0 0.5 0.5 ! Data comment
! End comment""")
    data = read_snp(str(d))
    assert len(data.frequency) == 1
    assert data.frequency[0] == 1e9
