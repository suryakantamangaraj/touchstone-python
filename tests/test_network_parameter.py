import pytest
from touchstone.parser import db_to_mag, mag_to_db, deg_to_rad, rad_to_deg


def test_network_parameter_conversions():
    assert db_to_mag(20) == 10.0
    assert mag_to_db(10) == 20.0
    assert deg_to_rad(180) == pytest.approx(3.14159, 0.001)
    assert rad_to_deg(3.14159) == pytest.approx(180.0, 0.001)
