import pytest

from touchstone.parser import normalize_frequency


def test_frequency_converter():
    assert normalize_frequency(1, "HZ") == 1.0
    assert normalize_frequency(1, "KHZ") == 1000.0
    assert normalize_frequency(1, "MHZ") == 1e6
    assert normalize_frequency(1, "GHZ") == 1e9
