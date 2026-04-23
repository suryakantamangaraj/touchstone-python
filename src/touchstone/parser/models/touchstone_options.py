"""
Data classes representing options parsed from Touchstone files.

The option line (beginning with ``#``) in a Touchstone file specifies the
frequency unit, parameter type, data format, and reference impedance.
This module defines the :class:`TouchstoneOptions` dataclass to hold
those parsed values.
"""

from dataclasses import dataclass

from .data_format import DataFormat
from .frequency_unit import FrequencyUnit
from .parameter_type import ParameterType


@dataclass(frozen=True)
class TouchstoneOptions:
    """Represents the option line configuration parsed from a Touchstone file.

    A Touchstone option line has the form::

        # <frequency_unit> <parameter_type> <data_format> R <impedance>

    For example: ``# GHz S MA R 50``

    Attributes:
        frequency_unit: The frequency unit for data points.
            Defaults to :attr:`~FrequencyUnit.GHZ`.
        parameter_type: The network parameter type.
            Defaults to :attr:`~ParameterType.S`.
        data_format: The data format for parameter values.
            Defaults to :attr:`~DataFormat.MA`.
        reference_impedance: The reference impedance in ohms.
            Defaults to ``50.0``.
    """

    frequency_unit: FrequencyUnit = FrequencyUnit.GHZ
    parameter_type: ParameterType = ParameterType.S
    data_format: DataFormat = DataFormat.MA
    reference_impedance: float = 50.0

    def __str__(self) -> str:
        """Return the option line string representation.

        Returns:
            str: A string formatted as a Touchstone option line,
            e.g. ``# GHZ S MA R 50.0``.
        """
        return (
            f"# {self.frequency_unit.name} {self.parameter_type.name} "
            f"{self.data_format.name} R {self.reference_impedance}"
        )

    @classmethod
    def default(cls) -> "TouchstoneOptions":
        """Create a TouchstoneOptions instance with default values.

        Returns:
            TouchstoneOptions: Default options (GHz, S, MA, 50 Ω).
        """
        return cls()
