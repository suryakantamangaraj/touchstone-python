import pytest

from touchstone.parser.parsing.option_line_parser import OptionLineParser


def test_option_line_parser():
    options = OptionLineParser.parse("# MHZ Y RI R 75")
    assert options.frequency_unit.name == "MHZ"
    assert options.parameter_type.name == "Y"
    assert options.data_format.name == "RI"
    assert options.reference_impedance == 75.0


def test_minimal_option_line_uses_defaults():
    options = OptionLineParser.parse("#")
    assert options.frequency_unit.name == "GHZ"
    assert options.parameter_type.name == "S"
    assert options.data_format.name == "MA"
    assert options.reference_impedance == 50.0


def test_lower_case_parses_correctly():
    options = OptionLineParser.parse("# mhz y ri r 75")
    assert options.frequency_unit.name == "MHZ"
    assert options.parameter_type.name == "Y"
    assert options.data_format.name == "RI"
    assert options.reference_impedance == 75.0


def test_with_inline_comment_ignores_comment():
    options = OptionLineParser.parse("# MHZ Y RI R 75 ! This is a comment")
    assert options.frequency_unit.name == "MHZ"
    assert options.reference_impedance == 75.0


def test_hybrid_parameters():
    options = OptionLineParser.parse("# GHZ H MA")
    assert options.parameter_type.name == "H"


def test_inverse_hybrid_parameters():
    options = OptionLineParser.parse("# GHZ G MA")
    assert options.parameter_type.name == "G"


def test_invalid_impedance_throws():
    with pytest.raises(ValueError):
        OptionLineParser.parse("# GHZ S MA R abc")


def test_missing_impedance_value():
    options = OptionLineParser.parse("# GHZ S MA R")
    # Current implementation gracefully ignores missing value
    assert options.reference_impedance == 50.0


def test_options_to_string():
    from touchstone.parser.models.touchstone_options import TouchstoneOptions

    options = TouchstoneOptions.default()
    assert str(options) == "# GHZ S MA R 50.0"
