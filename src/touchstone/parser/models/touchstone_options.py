"""
Data classes representing options parsed from Touchstone files.
"""

from dataclasses import dataclass

from .data_format import DataFormat
from .frequency_unit import FrequencyUnit
from .parameter_type import ParameterType


@dataclass(frozen=True)
class TouchstoneOptions:
    """
    Represents the option line configuration parsed from a Touchstone file.
    """

    frequency_unit: FrequencyUnit = FrequencyUnit.GHZ
    parameter_type: ParameterType = ParameterType.S
    data_format: DataFormat = DataFormat.MA
    reference_impedance: float = 50.0

    def __str__(self) -> str:
        return (
            f"# {self.frequency_unit.name} {self.parameter_type.name} "
            f"{self.data_format.name} R {self.reference_impedance}"
        )
