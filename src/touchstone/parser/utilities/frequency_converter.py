"""
Utility for frequency conversions.
"""

from typing import Union

from ..models.frequency_unit import FrequencyUnit


def get_multiplier(unit: Union[str, FrequencyUnit]) -> float:
    """Get the multiplier for a given frequency unit to Hz."""
    if isinstance(unit, FrequencyUnit):
        unit = unit.name
    units = {"HZ": 1.0, "KHZ": 1e3, "MHZ": 1e6, "GHZ": 1e9}
    return units.get(unit.upper(), 1.0)


def normalize_frequency(freq: float, unit: Union[str, FrequencyUnit]) -> float:
    """
    Normalize frequency to Hz.

    Args:
        freq (float): The frequency value.
        unit (str | FrequencyUnit): The frequency unit (e.g., 'Hz', 'kHz').

    Returns:
        float: The frequency in Hz.
    """
    return freq * get_multiplier(unit)


def from_hz(value: float, unit: Union[str, FrequencyUnit]) -> float:
    """Convert a frequency value from Hz to the specified unit."""
    return value / get_multiplier(unit)


def convert(
    value: float,
    from_unit: Union[str, FrequencyUnit],
    to_unit: Union[str, FrequencyUnit],
) -> float:
    """Convert a frequency value between two units."""
    hz = value * get_multiplier(from_unit)
    return from_hz(hz, to_unit)
