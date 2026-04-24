import pytest

from touchstone.parser import db_to_mag, deg_to_rad, mag_to_db, rad_to_deg
from touchstone.parser.models.network_parameter import NetworkParameter


def test_network_parameter_conversions():
    assert db_to_mag(20) == 10.0
    assert mag_to_db(10) == 20.0
    assert deg_to_rad(180) == pytest.approx(3.14159, 0.001)
    assert rad_to_deg(3.14159) == pytest.approx(180.0, 0.001)


def test_from_real_imaginary():
    np = NetworkParameter.from_real_imaginary(3.0, 4.0)
    assert np.real == 3.0
    assert np.imaginary == 4.0
    assert np.magnitude == 5.0


def test_from_magnitude_angle_0():
    np = NetworkParameter.from_magnitude_angle(5.0, 0.0)
    assert pytest.approx(np.real) == 5.0
    assert pytest.approx(np.imaginary) == 0.0
    assert pytest.approx(np.magnitude) == 5.0
    assert pytest.approx(np.phase_degrees) == 0.0


def test_from_magnitude_angle_90():
    np = NetworkParameter.from_magnitude_angle(5.0, 90.0)
    assert pytest.approx(np.real) == 0.0
    assert pytest.approx(np.imaginary) == 5.0


def test_from_decibel_angle_0():
    np = NetworkParameter.from_decibel_angle(0.0, 0.0)
    assert pytest.approx(np.magnitude) == 1.0


def test_from_decibel_angle_minus_20():
    np = NetworkParameter.from_decibel_angle(-20.0, 0.0)
    assert pytest.approx(np.magnitude) == 0.1


def test_magnitude_db_zero():
    np = NetworkParameter.from_real_imaginary(0.0, 0.0)
    assert np.magnitude_db == float("-inf")


def test_conjugate():
    np = NetworkParameter.from_real_imaginary(3.0, 4.0)
    conj = np.conjugate()
    assert conj.real == 3.0
    assert conj.imaginary == -4.0


def test_reciprocal():
    np = NetworkParameter.from_real_imaginary(2.0, 0.0)
    recip = np.reciprocal()
    assert recip.real == 0.5
    assert recip.imaginary == 0.0


def test_reciprocal_zero():
    np = NetworkParameter.from_real_imaginary(0.0, 0.0)
    with pytest.raises(ZeroDivisionError):
        np.reciprocal()


def test_add():
    np1 = NetworkParameter.from_real_imaginary(1.0, 2.0)
    np2 = NetworkParameter.from_real_imaginary(3.0, 4.0)
    res = np1 + np2
    assert res.real == 4.0
    assert res.imaginary == 6.0


def test_multiply():
    np1 = NetworkParameter.from_real_imaginary(1.0, 2.0)
    np2 = NetworkParameter.from_real_imaginary(3.0, 4.0)
    # (1+2i)(3+4i) = 3 + 4i + 6i - 8 = -5 + 10i
    res = np1 * np2
    assert res.real == -5.0
    assert res.imaginary == 10.0


def test_equality():
    np1 = NetworkParameter.from_real_imaginary(1.0, 2.0)
    np2 = NetworkParameter.from_real_imaginary(1.0, 2.0)
    assert np1 == np2


def test_approximately_equals():
    np1 = NetworkParameter.from_real_imaginary(1.0, 2.0)
    np2 = NetworkParameter.from_real_imaginary(1.0000000001, 2.0)
    assert np1.approximately_equals(np2)
    assert not np1 == np2
