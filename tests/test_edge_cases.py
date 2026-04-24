"""Edge case tests for the Touchstone parser.

Port of the .NET EdgeCaseTests to Python, covering:
- Empty input, comment-only input
- Duplicate option lines
- Invalid numeric data
- Model validation (zero ports, null options, negative frequency)
- Inline comments in data lines
- Mixed-case option lines
- Extra whitespace handling
- Tab-separated values
- Null/empty path handling
"""

import numpy as np
import pytest

from touchstone.parser import (
    TouchstoneData,
    TouchstoneParser,
    TouchstoneParserException,
)
from touchstone.parser.models.frequency_point import FrequencyPoint
from touchstone.parser.models.frequency_unit import FrequencyUnit
from touchstone.parser.models.network_parameter import NetworkParameter


# ──────────────────────────────────────────────────────────────────
#  Empty / Minimal Input
# ──────────────────────────────────────────────────────────────────


class TestEmptyInput:
    """Edge cases for empty and minimal inputs."""

    def test_empty_string_with_known_port_count(self):
        data = TouchstoneParser.parse_string("", n_ports=2)
        assert data.n_freq == 0
        assert data.n_ports == 2

    def test_only_comments_with_known_port_count(self):
        data = TouchstoneParser.parse_string(
            "! comment 1\n! comment 2\n", n_ports=1
        )
        assert data.n_ports == 1
        assert data.n_freq == 0
        assert len(data.comments) == 2

    def test_only_comments_returns_empty(self):
        data = TouchstoneParser.parse_string("! Just a comment", n_ports=1)
        assert data.n_freq == 0


# ──────────────────────────────────────────────────────────────────
#  Parser Errors
# ──────────────────────────────────────────────────────────────────


class TestParserErrors:
    """Edge cases that should raise exceptions."""

    def test_duplicate_option_line_throws(self):
        content = "# GHZ S MA R 50\n# GHZ S MA R 50\n50 1 0"
        with pytest.raises(TouchstoneParserException, match="Multiple option lines"):
            TouchstoneParser.parse_string(content)

    def test_invalid_numeric_data_throws(self):
        content = "# GHZ S MA R 50\n50 abc def"
        with pytest.raises(TouchstoneParserException, match="Invalid numeric value"):
            TouchstoneParser.parse_string(content)

    def test_missing_file_throws(self):
        with pytest.raises(Exception):
            TouchstoneParser.parse("nonexistent_file.s1p")

    def test_null_path_throws(self):
        with pytest.raises(ValueError):
            TouchstoneParser.parse("")

    def test_detect_port_count_empty_throws(self):
        with pytest.raises(ValueError):
            TouchstoneParser.detect_port_count("")


# ──────────────────────────────────────────────────────────────────
#  Model Validation
# ──────────────────────────────────────────────────────────────────


class TestModelValidation:
    """Edge cases for model constructors."""

    def test_touchstone_data_zero_ports_throws(self):
        with pytest.raises(ValueError, match="Number of ports must be >= 1"):
            TouchstoneData(
                frequency=np.array([]),
                s_parameters=np.zeros((0, 0, 0), dtype=complex),
            )

    def test_touchstone_data_null_options_throws(self):
        with pytest.raises(ValueError, match="options cannot be None"):
            TouchstoneData(
                frequency=np.array([]),
                s_parameters=np.zeros((0, 1, 1), dtype=complex),
                options=None,
            )

    def test_frequency_point_negative_frequency_throws(self):
        with pytest.raises(ValueError, match="negative"):
            FrequencyPoint(
                frequency_hz=-1.0,
                _s_parameters=np.array([[0j]]),
            )

    def test_frequency_point_non_square_matrix_throws(self):
        with pytest.raises(ValueError, match="square"):
            FrequencyPoint(
                frequency_hz=1.0,
                _s_parameters=np.zeros((2, 3), dtype=complex),
            )

    def test_frequency_point_index_out_of_range_throws(self):
        fp = FrequencyPoint(
            frequency_hz=1.0,
            _s_parameters=np.array([[0j]]),
        )
        with pytest.raises(IndexError):
            _ = fp[1, 0]

    def test_network_parameter_reciprocal_of_zero_throws(self):
        param = NetworkParameter(0j)
        with pytest.raises(ZeroDivisionError):
            param.reciprocal()

    def test_touchstone_data_mismatched_lengths_throws(self):
        with pytest.raises(ValueError, match="must match"):
            TouchstoneData(
                frequency=np.array([1.0, 2.0]),
                s_parameters=np.zeros((3, 1, 1), dtype=complex),
            )


# ──────────────────────────────────────────────────────────────────
#  Inline Comments & Whitespace
# ──────────────────────────────────────────────────────────────────


class TestWhitespaceAndComments:
    """Edge cases for whitespace handling and inline comments."""

    def test_inline_comment_in_data_handled_correctly(self):
        content = "# GHZ S RI R 50\n1.0 0.1 0.2 ! inline comment"
        data = TouchstoneParser.parse_string(content, n_ports=1)
        assert data.n_freq == 1
        s11 = data.s_parameters[0, 0, 0]
        assert s11.real == pytest.approx(0.1, abs=1e-10)
        assert s11.imag == pytest.approx(0.2, abs=1e-10)

    def test_mixed_case_options_parses_correctly(self):
        content = "# mHz s ri r 50\n100 0.5 0.3"
        data = TouchstoneParser.parse_string(content, n_ports=1)
        assert data.options.frequency_unit == FrequencyUnit.MHZ

    def test_extra_whitespace_parses_correctly(self):
        content = "  #   GHZ   S   RI   R   50  \n  1.0     0.1    0.2  "
        data = TouchstoneParser.parse_string(content, n_ports=1)
        assert data.n_freq == 1
        s11 = data.s_parameters[0, 0, 0]
        assert s11.real == pytest.approx(0.1, abs=1e-10)
        assert s11.imag == pytest.approx(0.2, abs=1e-10)

    def test_tab_separated_values_parses_correctly(self):
        content = "# GHZ S RI R 50\n1.0\t0.1\t0.2"
        data = TouchstoneParser.parse_string(content, n_ports=1)
        assert data.n_freq == 1
        s11 = data.s_parameters[0, 0, 0]
        assert s11.real == pytest.approx(0.1, abs=1e-10)

    def test_multiple_blank_lines_ignored(self):
        content = "# GHZ S RI R 50\n\n\n1.0 0.1 0.2\n\n\n2.0 0.3 0.4\n\n"
        data = TouchstoneParser.parse_string(content, n_ports=1)
        assert data.n_freq == 2

    def test_comment_with_special_characters(self):
        content = "! Temp: 25°C, σ=0.01\n# GHZ S RI R 50\n1.0 0.1 0.2"
        data = TouchstoneParser.parse_string(content, n_ports=1)
        assert len(data.comments) >= 1
        assert "25°C" in data.comments[0]

    def test_option_line_with_inline_comment(self):
        content = "# GHZ S RI R 50 ! this is a comment\n1.0 0.1 0.2"
        data = TouchstoneParser.parse_string(content, n_ports=1)
        assert data.n_freq == 1
        assert data.options.frequency_unit == FrequencyUnit.GHZ


# ──────────────────────────────────────────────────────────────────
#  Data Format Variants
# ──────────────────────────────────────────────────────────────────


class TestDataFormats:
    """Tests for all three data format variants."""

    def test_ri_format_parses_correctly(self):
        content = "# GHZ S RI R 50\n1.0 0.5 -0.3"
        data = TouchstoneParser.parse_string(content, n_ports=1)
        s11 = data.s_parameters[0, 0, 0]
        assert s11.real == pytest.approx(0.5, abs=1e-10)
        assert s11.imag == pytest.approx(-0.3, abs=1e-10)

    def test_ma_format_parses_correctly(self):
        content = "# GHZ S MA R 50\n1.0 0.5 45.0"
        data = TouchstoneParser.parse_string(content, n_ports=1)
        s11 = data.s_parameters[0, 0, 0]
        assert abs(s11) == pytest.approx(0.5, abs=1e-6)

    def test_db_format_parses_correctly(self):
        content = "# GHZ S DB R 50\n1.0 -6.0 0.0"
        data = TouchstoneParser.parse_string(content, n_ports=1)
        s11 = data.s_parameters[0, 0, 0]
        # -6 dB ≈ 0.5012 magnitude
        assert abs(s11) == pytest.approx(10 ** (-6.0 / 20.0), abs=1e-4)
