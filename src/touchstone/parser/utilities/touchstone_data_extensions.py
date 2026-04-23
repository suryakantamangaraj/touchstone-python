"""
Extension methods for analyzing TouchstoneData objects.

This module provides standalone functions for common RF analysis tasks
such as extracting magnitude and phase, computing insertion loss, return
loss, VSWR, filtering by frequency range, and accessing specific
S-parameter indices.
"""

import numpy as np

from ..models.touchstone_data import TouchstoneData
from .network_parameter_extensions import mag_to_db, rad_to_deg


def get_magnitude(
    data: TouchstoneData, to_port: int, from_port: int, db: bool = True
) -> np.ndarray:
    """Get magnitude of S-parameters across all frequencies.

    Args:
        data: The Touchstone data to analyze.
        to_port: The target (output) port, **1-indexed**.
        from_port: The source (input) port, **1-indexed**.
        db: If ``True``, returns magnitude in dB. If ``False``,
            returns linear magnitude. Defaults to ``True``.

    Returns:
        numpy.ndarray: Array of magnitude values.

    Example:
        >>> mag_db = get_magnitude(data, 2, 1, db=True)
    """
    s = data.get_s(to_port, from_port)
    mag = np.abs(s)
    return mag_to_db(mag) if db else mag


def get_phase(
    data: TouchstoneData, to_port: int, from_port: int, deg: bool = True
) -> np.ndarray:
    """Get phase of S-parameters across all frequencies.

    Args:
        data: The Touchstone data to analyze.
        to_port: The target (output) port, **1-indexed**.
        from_port: The source (input) port, **1-indexed**.
        deg: If ``True``, returns phase in degrees. If ``False``,
            returns phase in radians. Defaults to ``True``.

    Returns:
        numpy.ndarray: Array of phase values.

    Example:
        >>> phase_deg = get_phase(data, 1, 1, deg=True)
    """
    s = data.get_s(to_port, from_port)
    phase = np.angle(s)
    return rad_to_deg(phase) if deg else phase


def to_insertion_loss(data: TouchstoneData) -> np.ndarray:
    """Compute insertion loss from S21.

    Insertion loss is ``-|S21|`` in dB, so that positive values
    indicate signal attenuation.

    Args:
        data: The Touchstone data (must have ≥ 2 ports).

    Returns:
        numpy.ndarray: Array of insertion loss values in dB.

    Raises:
        ValueError: If the data has fewer than 2 ports.
    """
    if data.n_ports < 2:
        raise ValueError("Insertion loss requires at least 2 ports.")
    return -get_magnitude(data, 2, 1, db=True)


def to_return_loss(data: TouchstoneData) -> np.ndarray:
    """Compute return loss from S11.

    Return loss is ``-|S11|`` in dB, so that positive values
    indicate better impedance matching.

    Args:
        data: The Touchstone data.

    Returns:
        numpy.ndarray: Array of return loss values in dB.
    """
    return -get_magnitude(data, 1, 1, db=True)


def to_vswr(data: TouchstoneData) -> np.ndarray:
    """Compute VSWR (Voltage Standing Wave Ratio) from S11.

    VSWR is calculated as ``(1 + |S11|) / (1 - |S11|)``.

    Args:
        data: The Touchstone data.

    Returns:
        numpy.ndarray: Array of VSWR values (dimensionless, ≥ 1.0).
    """
    from .network_parameter_extensions import vswr_from_s11

    s11 = data.get_s(1, 1)
    return vswr_from_s11(s11)


def in_frequency_range(
    data: TouchstoneData, min_hz: float, max_hz: float
) -> TouchstoneData:
    """Filter data to a specific frequency range in Hz.

    Creates a new :class:`TouchstoneData` containing only the frequency
    points within ``[min_hz, max_hz]`` (inclusive).

    Args:
        data: The original Touchstone data.
        min_hz: Minimum frequency in Hz (inclusive).
        max_hz: Maximum frequency in Hz (inclusive).

    Returns:
        TouchstoneData: A new filtered instance.

    Example:
        >>> passband = in_frequency_range(data, 2e9, 3e9)
    """
    mask = (data.frequency >= min_hz) & (data.frequency <= max_hz)
    return TouchstoneData(
        frequency=data.frequency[mask],
        s_parameters=data.s_parameters[mask],
        options=data.options,
        comments=data.comments,
        filename=data.filename,
        metadata=data.metadata,
    )


def get_s11(data: TouchstoneData):
    """Get an iterable of ``(frequency_hz, NetworkParameter)`` for S11.

    Convenience shortcut for ``data.get_parameter(1, 1)``.

    Args:
        data: The Touchstone data.

    Returns:
        Iterable[tuple[float, NetworkParameter]]: Frequency/parameter pairs.
    """
    return data.get_parameter(1, 1)


def get_s21(data: TouchstoneData):
    """Get an iterable of ``(frequency_hz, NetworkParameter)`` for S21.

    Convenience shortcut for ``data.get_parameter(2, 1)``.

    Args:
        data: The Touchstone data (must have ≥ 2 ports).

    Returns:
        Iterable[tuple[float, NetworkParameter]]: Frequency/parameter pairs.
    """
    return data.get_parameter(2, 1)


def get_s12(data: TouchstoneData):
    """Get an iterable of ``(frequency_hz, NetworkParameter)`` for S12.

    Convenience shortcut for ``data.get_parameter(1, 2)``.

    Args:
        data: The Touchstone data (must have ≥ 2 ports).

    Returns:
        Iterable[tuple[float, NetworkParameter]]: Frequency/parameter pairs.
    """
    return data.get_parameter(1, 2)


def get_s22(data: TouchstoneData):
    """Get an iterable of ``(frequency_hz, NetworkParameter)`` for S22.

    Convenience shortcut for ``data.get_parameter(2, 2)``.

    Args:
        data: The Touchstone data (must have ≥ 2 ports).

    Returns:
        Iterable[tuple[float, NetworkParameter]]: Frequency/parameter pairs.
    """
    return data.get_parameter(2, 2)


def get_frequencies_in(data: TouchstoneData, unit) -> np.ndarray:
    """Get all frequencies converted to the specified unit.

    Args:
        data: The Touchstone data.
        unit: The target frequency unit (string or
            :class:`~touchstone.parser.models.frequency_unit.FrequencyUnit`).

    Returns:
        numpy.ndarray: Array of frequency values in the specified unit.

    Example:
        >>> freqs_ghz = get_frequencies_in(data, "GHz")
    """
    from .frequency_converter import get_multiplier

    return data.frequency / get_multiplier(unit)


def min_frequency_hz(data: TouchstoneData) -> float:
    """Get the minimum frequency in Hz.

    Args:
        data: The Touchstone data.

    Returns:
        float: The minimum frequency value.

    Raises:
        ValueError: If the data contains no frequency points.
    """
    if data.n_freq == 0:
        raise ValueError("Touchstone data contains no frequency points.")
    return float(np.min(data.frequency))


def max_frequency_hz(data: TouchstoneData) -> float:
    """Get the maximum frequency in Hz.

    Args:
        data: The Touchstone data.

    Returns:
        float: The maximum frequency value.

    Raises:
        ValueError: If the data contains no frequency points.
    """
    if data.n_freq == 0:
        raise ValueError("Touchstone data contains no frequency points.")
    return float(np.max(data.frequency))
