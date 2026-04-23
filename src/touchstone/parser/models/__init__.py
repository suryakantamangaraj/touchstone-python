"""
Domain models for Touchstone file data structures.

This sub-package contains all the core data classes and enumerations used
to represent parsed Touchstone data:

- :class:`~touchstone.parser.models.touchstone_data.TouchstoneData` — The main parsed data container.
- :class:`~touchstone.parser.models.touchstone_options.TouchstoneOptions` — Option line configuration.
- :class:`~touchstone.parser.models.network_parameter.NetworkParameter` — A single complex S-parameter.
- :class:`~touchstone.parser.models.frequency_point.FrequencyPoint` — A single frequency point with its S-matrix.
- :class:`~touchstone.parser.models.data_format.DataFormat` — Data format enumeration (RI, MA, DB).
- :class:`~touchstone.parser.models.frequency_unit.FrequencyUnit` — Frequency unit enumeration (Hz, kHz, MHz, GHz).
- :class:`~touchstone.parser.models.parameter_type.ParameterType` — Parameter type enumeration (S, Y, Z, G, H).
"""

from .data_format import DataFormat
from .frequency_point import FrequencyPoint
from .frequency_unit import FrequencyUnit
from .network_parameter import NetworkParameter
from .parameter_type import ParameterType
from .touchstone_data import TouchstoneData
from .touchstone_options import TouchstoneOptions

__all__ = [
    "DataFormat",
    "FrequencyPoint",
    "FrequencyUnit",
    "NetworkParameter",
    "ParameterType",
    "TouchstoneData",
    "TouchstoneOptions",
]
