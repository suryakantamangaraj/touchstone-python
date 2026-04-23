"""
Utility for frequency conversions.

This module provides functions to convert frequency values between
different units (Hz, kHz, MHz, GHz) and to normalize frequencies to Hz.
"""

from typing import Union

from ..models.frequency_unit import FrequencyUnit


def get_multiplier(unit: Union[str, FrequencyUnit]) -> float:
    """Get the multiplier to convert a frequency value to Hz.

    Args:
        unit: A frequency unit as a string (``'Hz'``, ``'kHz'``,
            ``'MHz'``, ``'GHz'``) or a :class:`FrequencyUnit` enum member.

    Returns:
        float: The multiplier (e.g., ``1e9`` for GHz). Returns ``1.0``
        for unrecognized units.

    Example:
        >>> get_multiplier("GHz")
        1000000000.0
        >>> get_multiplier(FrequencyUnit.MHZ)
        1000000.0
    """
    if isinstance(unit, FrequencyUnit):
        unit = unit.name
    units = {"HZ": 1.0, "KHZ": 1e3, "MHZ": 1e6, "GHZ": 1e9}
    return units.get(unit.upper(), 1.0)


def normalize_frequency(freq: float, unit: Union[str, FrequencyUnit]) -> float:
    """Normalize a frequency value to Hz.

    Multiplies the given frequency by the appropriate unit multiplier
    to convert it to Hertz.

    Args:
        freq: The frequency value in the specified unit.
        unit: The frequency unit (e.g., ``'GHz'`` or
            :attr:`FrequencyUnit.GHZ`).

    Returns:
        float: The frequency in Hz.

    Example:
        >>> normalize_frequency(2.4, "GHz")
        2400000000.0
    """
    return freq * get_multiplier(unit)


def from_hz(value: float, unit: Union[str, FrequencyUnit]) -> float:
    """Convert a frequency value from Hz to the specified unit.

    Args:
        value: The frequency in Hz.
        unit: The target frequency unit (e.g., ``'MHz'`` or
            :attr:`FrequencyUnit.MHZ`).

    Returns:
        float: The frequency in the target unit.

    Example:
        >>> from_hz(2.4e9, "GHz")
        2.4
    """
    return value / get_multiplier(unit)


def convert(
    value: float,
    from_unit: Union[str, FrequencyUnit],
    to_unit: Union[str, FrequencyUnit],
) -> float:
    """Convert a frequency value from one unit to another.

    Internally normalizes to Hz and then converts to the target unit.

    Args:
        value: The frequency value in ``from_unit``.
        from_unit: The source frequency unit.
        to_unit: The destination frequency unit.

    Returns:
        float: The frequency in ``to_unit``.

    Example:
        >>> convert(2400, "MHz", "GHz")
        2.4
    """
    hz = value * get_multiplier(from_unit)
    return from_hz(hz, to_unit)
