"""Comprehensive integration tests for TouchstoneParser.

Port of the .NET TouchstoneParserTests to Python, covering:
- 1-port, 2-port, 3-port parsing
- All data formats (RI, MA, DB)
- All API overloads (file, string, stream, async)
- Port detection
- Comments extraction
- Edge cases (minimal files, no option line)
"""

import asyncio
import io
import math
import os

import pytest

from touchstone.parser import TouchstoneParser
from touchstone.parser.models.data_format import DataFormat
from touchstone.parser.models.frequency_unit import FrequencyUnit

TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), "test_data")


def get_test_file(filename: str) -> str:
    return os.path.join(TEST_DATA_DIR, filename)


# ──────────────────────────────────────────────────────────────────
#  1-Port Tests
# ──────────────────────────────────────────────────────────────────


class TestParse1Port:
    """Integration tests for 1-port Touchstone files."""

    def test_parse_simple_1port_parses_correctly(self):
        data = TouchstoneParser.parse(get_test_file("simple.s1p"))

        assert data.n_ports == 1
        assert data.n_freq == 5
        assert data.options.frequency_unit == FrequencyUnit.MHZ
        assert data.options.data_format == DataFormat.RI
        assert data.options.reference_impedance == 50.0
        assert data.filename == "simple.s1p"

    def test_parse_simple_1port_frequencies_are_in_hz(self):
        data = TouchstoneParser.parse(get_test_file("simple.s1p"))

        # File uses MHz, first point is 100 MHz = 100e6 Hz
        assert data.frequency[0] == pytest.approx(100e6)
        assert data.frequency[1] == pytest.approx(200e6)
        assert data.frequency[4] == pytest.approx(2000e6)

    def test_parse_simple_1port_parameter_values_are_correct(self):
        data = TouchstoneParser.parse(get_test_file("simple.s1p"))

        # First point: S11 = 0.01 + 0.02j (RI format)
        s11 = data.s_parameters[0, 0, 0]
        assert s11.real == pytest.approx(0.01, abs=1e-10)
        assert s11.imag == pytest.approx(0.02, abs=1e-10)

    def test_parse_simple_1port_comments_extracted(self):
        data = TouchstoneParser.parse(get_test_file("simple.s1p"))

        assert len(data.comments) >= 3
        assert "Simple 1-port" in data.comments[0]


# ──────────────────────────────────────────────────────────────────
#  2-Port Tests
# ──────────────────────────────────────────────────────────────────


class TestParse2Port:
    """Integration tests for 2-port Touchstone files."""

    def test_parse_bandpass_filter_parses_correctly(self):
        data = TouchstoneParser.parse(get_test_file("bandpass_filter.s2p"))

        assert data.n_ports == 2
        assert data.n_freq == 6
        assert data.options.frequency_unit == FrequencyUnit.GHZ
        assert data.options.data_format == DataFormat.DB

    def test_parse_bandpass_filter_2port_ordering(self):
        """Verify legacy 2-port ordering: S11, S21, S12, S22."""
        data = TouchstoneParser.parse(get_test_file("bandpass_filter.s2p"))

        # At 1.0 GHz (3rd point, index 2):
        # S11=-25dB, S21=-0.5dB, S12=-0.6dB, S22=-24dB
        _ = data[2]

        # S11 magnitude in dB
        s11_db = 20 * math.log10(abs(data.s_parameters[2, 0, 0]))
        assert s11_db == pytest.approx(-25.0, abs=0.1)

        # S21 magnitude in dB
        s21_db = 20 * math.log10(abs(data.s_parameters[2, 1, 0]))
        assert s21_db == pytest.approx(-0.5, abs=0.1)

        # S12 magnitude in dB
        s12_db = 20 * math.log10(abs(data.s_parameters[2, 0, 1]))
        assert s12_db == pytest.approx(-0.6, abs=0.1)

        # S22 magnitude in dB
        s22_db = 20 * math.log10(abs(data.s_parameters[2, 1, 1]))
        assert s22_db == pytest.approx(-24.0, abs=0.1)

    def test_parse_amplifier_ri_format(self):
        """Verify Real-Imaginary format parsing."""
        data = TouchstoneParser.parse(get_test_file("amplifier.s2p"))

        assert data.n_ports == 2
        assert data.n_freq == 5
        assert data.options.data_format == DataFormat.RI

        # First point: S11 = 0.3926 - 0.1211j
        s11 = data.s_parameters[0, 0, 0]
        assert s11.real == pytest.approx(0.3926, abs=1e-4)
        assert s11.imag == pytest.approx(-0.1211, abs=1e-4)


# ──────────────────────────────────────────────────────────────────
#  3-Port Tests
# ──────────────────────────────────────────────────────────────────


class TestParse3Port:
    """Integration tests for 3-port Touchstone files."""

    def test_parse_coupler_3port_parses_correctly(self):
        data = TouchstoneParser.parse(get_test_file("coupler.s3p"))

        assert data.n_ports == 3
        assert data.n_freq == 2
        assert data.options.data_format == DataFormat.MA

    def test_parse_coupler_3port_matrix_values(self):
        data = TouchstoneParser.parse(get_test_file("coupler.s3p"))

        # First frequency point: S11 magnitude = 0.1
        s11_mag = abs(data.s_parameters[0, 0, 0])
        assert s11_mag == pytest.approx(0.1, abs=1e-6)

        # S12 magnitude = 0.95
        s12_mag = abs(data.s_parameters[0, 0, 1])
        assert s12_mag == pytest.approx(0.95, abs=1e-6)


# ──────────────────────────────────────────────────────────────────
#  Special Cases
# ──────────────────────────────────────────────────────────────────


class TestSpecialCases:
    """Tests for comments, minimal files, and defaults."""

    def test_parse_comments_file_extracts_all_comments(self):
        data = TouchstoneParser.parse(get_test_file("comments_only.s2p"))

        assert len(data.comments) >= 10
        assert any("Keysight PNA-X" in c for c in data.comments)

    def test_parse_minimal_file_parses_correctly(self):
        data = TouchstoneParser.parse(get_test_file("minimal.s2p"))

        assert data.n_ports == 2
        assert data.n_freq == 1
        assert len(data.comments) == 0

    def test_parse_no_option_line_uses_defaults(self):
        data = TouchstoneParser.parse(get_test_file("no_option_line.s1p"))

        assert data.n_ports == 1
        assert data.n_freq == 3
        # Default: GHz S MA R 50
        assert data.options.frequency_unit == FrequencyUnit.GHZ
        assert data.options.data_format == DataFormat.MA
        assert data.options.reference_impedance == 50.0


# ──────────────────────────────────────────────────────────────────
#  API Overloads
# ──────────────────────────────────────────────────────────────────


class TestAPIOverloads:
    """Tests for all parsing API surfaces."""

    def test_parse_string_parses_correctly(self):
        content = "# MHZ S RI R 50\n100 0.5 0.3"

        data = TouchstoneParser.parse_string(content, n_ports=1, filename="test.s1p")

        assert data.n_ports == 1
        assert data.n_freq == 1
        s11 = data.s_parameters[0, 0, 0]
        assert s11.real == pytest.approx(0.5, abs=1e-10)
        assert s11.imag == pytest.approx(0.3, abs=1e-10)

    def test_parse_stream_parses_correctly(self):
        content = "# GHZ S RI R 50\n1.0 0.1 0.2"
        stream = io.StringIO(content)

        data = TouchstoneParser.parse_stream(stream, filename="test.s1p")

        assert data.n_ports == 1
        assert data.n_freq == 1

    def test_parse_async_parses_correctly(self):
        filepath = get_test_file("simple.s1p")
        data = asyncio.run(TouchstoneParser.parse_async(filepath))

        assert data.n_ports == 1
        assert data.n_freq == 5

    def test_parse_nonexistent_file_raises(self):
        with pytest.raises(FileNotFoundError):
            TouchstoneParser.parse("nonexistent.s2p")


# ──────────────────────────────────────────────────────────────────
#  Port Detection
# ──────────────────────────────────────────────────────────────────


class TestPortDetection:
    """Tests for port count detection from filenames."""

    @pytest.mark.parametrize(
        "filename,expected",
        [
            ("test.s1p", 1),
            ("test.s2p", 2),
            ("test.s3p", 3),
            ("test.s4p", 4),
            ("test.S2P", 2),
            ("test.s12p", 12),
        ],
    )
    def test_detect_port_count_correctly_identifies_ports(self, filename, expected):
        assert TouchstoneParser.detect_port_count(filename) == expected

    def test_detect_port_count_invalid_extension_raises(self):
        with pytest.raises(Exception):
            TouchstoneParser.detect_port_count("test.txt")


# ──────────────────────────────────────────────────────────────────
#  LINQ-friendly API
# ──────────────────────────────────────────────────────────────────


class TestDataAccessAPI:
    """Tests for the data access and query API."""

    def test_get_parameter_returns_correct_iterable(self):
        data = TouchstoneParser.parse(get_test_file("simple.s1p"))

        s11_points = list(data.get_parameter(1, 1))

        assert len(s11_points) == 5
        freq, param = s11_points[0]
        assert freq == pytest.approx(100e6)
        assert param.real == pytest.approx(0.01, abs=1e-10)

    def test_frequencies_returns_all_frequencies(self):
        data = TouchstoneParser.parse(get_test_file("simple.s1p"))

        frequencies = list(data.frequencies)

        assert len(frequencies) == 5
        # Frequencies should be in ascending order
        assert all(
            frequencies[i] <= frequencies[i + 1] for i in range(len(frequencies) - 1)
        )

    def test_get_s_returns_correct_array(self):
        data = TouchstoneParser.parse(get_test_file("bandpass_filter.s2p"))

        s21 = data.get_s(2, 1)

        assert len(s21) == 6
        assert s21.dtype == complex

    def test_indexer_returns_frequency_point(self):
        data = TouchstoneParser.parse(get_test_file("simple.s1p"))

        point = data[0]

        assert point.frequency_hz == pytest.approx(100e6)
        assert point.number_of_ports == 1

    def test_count_property(self):
        data = TouchstoneParser.parse(get_test_file("simple.s1p"))
        assert data.count == data.n_freq == 5

    def test_where_filter(self):
        data = TouchstoneParser.parse(get_test_file("simple.s1p"))

        filtered = data.where(lambda pt: pt.frequency_hz >= 500e6)

        assert filtered.n_freq == 3  # 500, 1000, 2000 MHz

    def test_in_frequency_range(self):
        data = TouchstoneParser.parse(get_test_file("simple.s1p"))

        filtered = data.in_frequency_range(200e6, 1000e6)

        assert filtered.n_freq == 3  # 200, 500, 1000 MHz
