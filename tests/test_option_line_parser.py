import pytest
from touchstone.parser.parsing.option_line_parser import OptionLineParser


def test_option_line_parser():
    options = OptionLineParser.parse("# MHZ Y RI R 75")
    assert options.frequency_unit.name == "MHZ"
    assert options.parameter_type.name == "Y"
    assert options.data_format.name == "RI"
    assert options.reference_impedance == 75.0
