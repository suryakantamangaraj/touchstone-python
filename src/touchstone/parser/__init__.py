"""
Main package for parsing Touchstone (.sNp) files and analyzing S-parameters.

The ``touchstone.parser`` package is the primary public API surface. It
re-exports all important classes, functions, and enumerations so that
users can import directly from ``touchstone.parser``:

.. code-block:: python

    from touchstone.parser import TouchstoneParser, TouchstoneData
    from touchstone.parser import db_to_mag, normalize_frequency

Classes:
    TouchstoneParser: Static methods for parsing files, strings, and streams.
    TouchstoneData: The main container for parsed Touchstone data.
    TouchstoneOptions: Option line configuration (frequency unit, format, etc.).
    FrequencyUnit: Enumeration of supported frequency units.
    ParameterType: Enumeration of supported parameter types (S, Y, Z, G, H).
    DataFormat: Enumeration of supported data formats (RI, MA, DB).
    TouchstoneParserException: Exception raised for parse errors.

Functions:
    read_snp: Alias for :meth:`TouchstoneParser.parse`.
    parse_string: Alias for :meth:`TouchstoneParser.parse_string`.
    write_snp: Write data to a Touchstone file.
    write_snp_to_string: Convert data to a Touchstone format string.
    normalize_frequency: Convert a frequency value to Hz.
    db_to_mag: Convert dB to linear magnitude.
    mag_to_db: Convert linear magnitude to dB.
    deg_to_rad: Convert degrees to radians.
    rad_to_deg: Convert radians to degrees.
    ma_to_complex: Convert magnitude/angle to complex.
    db_to_complex: Convert dB/angle to complex.
    ri_to_complex: Convert real/imaginary to complex.
"""

from .models.data_format import DataFormat
from .models.frequency_unit import FrequencyUnit
from .models.parameter_type import ParameterType
from .models.touchstone_data import TouchstoneData
from .models.touchstone_options import TouchstoneOptions
from .parsing.touchstone_parser import TouchstoneParser
from .parsing.touchstone_parser_exception import TouchstoneParserException
from .utilities.frequency_converter import normalize_frequency
from .utilities.network_parameter_extensions import (
    db_to_complex,
    db_to_mag,
    deg_to_rad,
    ma_to_complex,
    mag_to_db,
    rad_to_deg,
    ri_to_complex,
)
from .utilities.touchstone_writer import write_snp, write_snp_to_string

# Maintain backward compatible function aliases
read_snp = TouchstoneParser.parse
"""Alias for :meth:`TouchstoneParser.parse` — parse a Touchstone file from disk."""

parse_string = TouchstoneParser.parse_string
"""Alias for :meth:`TouchstoneParser.parse_string` — parse Touchstone data from a string."""

__all__ = [
    "read_snp",
    "parse_string",
    "write_snp",
    "write_snp_to_string",
    "TouchstoneData",
    "TouchstoneOptions",
    "FrequencyUnit",
    "ParameterType",
    "DataFormat",
    "TouchstoneParser",
    "TouchstoneParserException",
    "normalize_frequency",
    "db_to_mag",
    "mag_to_db",
    "deg_to_rad",
    "rad_to_deg",
    "ma_to_complex",
    "db_to_complex",
    "ri_to_complex",
]
