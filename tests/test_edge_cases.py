import numpy as np
import pytest

from touchstone.parser import (
    TouchstoneData,
    TouchstoneParser,
    TouchstoneParserException,
)


def test_missing_file_throws():
    with pytest.raises(Exception):
        TouchstoneParser.parse("nonexistent_file.s1p")


def test_empty_string_with_known_port_count():
    data = TouchstoneParser.parse_string("", n_ports=2)
    assert data.n_freq == 0
    assert data.n_ports == 2


def test_only_comments_returns_empty():
    data = TouchstoneParser.parse_string("! Just a comment", n_ports=1)
    assert data.n_freq == 0


def test_duplicate_option_line_throws():
    content = "# GHZ S MA R 50\n# GHZ S MA R 50\n50 1 0"
    with pytest.raises(TouchstoneParserException, match="Multiple option lines"):
        TouchstoneParser.parse_string(content)


def test_invalid_numeric_data_throws():
    content = "# GHZ S MA R 50\n50 abc def"
    with pytest.raises(TouchstoneParserException, match="Invalid numeric value"):
        TouchstoneParser.parse_string(content)


def test_touchstone_data_zero_ports_throws():
    with pytest.raises(ValueError, match="Number of ports must be >= 1"):
        TouchstoneData(
            frequency=np.array([]), s_parameters=np.zeros((0, 0, 0), dtype=complex)
        )


def test_touchstone_data_null_options_throws():
    with pytest.raises(ValueError, match="options cannot be None"):
        TouchstoneData(
            frequency=np.array([]),
            s_parameters=np.zeros((0, 1, 1), dtype=complex),
            options=None,
        )


def test_null_path_throws():
    with pytest.raises(ValueError):
        TouchstoneParser.parse("")


def test_detect_port_count_null_throws():
    with pytest.raises(ValueError):
        TouchstoneParser.detect_port_count("")
