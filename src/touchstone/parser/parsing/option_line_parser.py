"""
Parser for the option line in Touchstone files.

The option line starts with ``#`` and specifies the frequency unit,
parameter type, data format, and reference impedance. This module
provides the :class:`OptionLineParser` class with a static
:meth:`~OptionLineParser.parse` method.
"""

from ..models.data_format import DataFormat
from ..models.frequency_unit import FrequencyUnit
from ..models.parameter_type import ParameterType
from ..models.touchstone_options import TouchstoneOptions


class OptionLineParser:
    """Parses the ``#`` option line from a Touchstone file.

    The option line format is::

        # <frequency_unit> <parameter_type> <data_format> R <impedance>

    Tokens can appear in any order. Missing tokens are filled with
    Touchstone defaults (GHz, S, MA, R 50).

    Example:
        >>> opts = OptionLineParser.parse("# GHz S MA R 50")
        >>> opts.frequency_unit
        <FrequencyUnit.GHZ: 'GHz'>
    """

    @staticmethod
    def parse(line: str) -> TouchstoneOptions:
        """Parse a Touchstone option line into a :class:`TouchstoneOptions` object.

        Args:
            line: The option line string, including the leading ``#``
                (e.g., ``'# GHz S MA R 50'``). Inline comments
                (text after ``!``) are stripped.

        Returns:
            TouchstoneOptions: The parsed options with all fields populated.
        """
        freq_unit = FrequencyUnit.GHZ
        param_type = ParameterType.S
        data_format = DataFormat.MA
        z0 = 50.0

        clean_line = line.split("!")[0].strip()
        if clean_line.startswith("#"):
            parts = clean_line[1:].strip().split()
            i = 0
            while i < len(parts):
                part = parts[i].upper()
                if part in ["HZ", "KHZ", "MHZ", "GHZ"]:
                    freq_unit = FrequencyUnit[part]
                elif part in ["S", "Y", "Z", "G", "H"]:
                    param_type = ParameterType[part]
                elif part in ["DB", "MA", "RI"]:
                    data_format = DataFormat[part]
                elif part == "R":
                    if i + 1 < len(parts):
                        z0 = float(parts[i + 1])
                        i += 1
                i += 1

        return TouchstoneOptions(
            frequency_unit=freq_unit,
            parameter_type=param_type,
            data_format=data_format,
            reference_impedance=z0,
        )
