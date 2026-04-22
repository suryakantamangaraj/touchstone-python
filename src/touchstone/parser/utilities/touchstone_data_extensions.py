"""
Extension methods for analyzing TouchstoneData objects.
"""

import numpy as np

from ..models.touchstone_data import TouchstoneData
from .network_parameter_extensions import mag_to_db, rad_to_deg


def get_magnitude(
    data: TouchstoneData, to_port: int, from_port: int, db: bool = True
) -> np.ndarray:
    """
    Get magnitude of S-parameters.

    Args:
        data (TouchstoneData): The Touchstone data.
        to_port (int): The target port (1-indexed).
        from_port (int): The source port (1-indexed).
        db (bool): If True, returns value in dB. Defaults to True.

    Returns:
        np.ndarray: Array of magnitude values.
    """
    s = data.get_s(to_port, from_port)
    mag = np.abs(s)
    return mag_to_db(mag) if db else mag


def get_phase(
    data: TouchstoneData, to_port: int, from_port: int, deg: bool = True
) -> np.ndarray:
    """
    Get phase of S-parameters.

    Args:
        data (TouchstoneData): The Touchstone data.
        to_port (int): The target port (1-indexed).
        from_port (int): The source port (1-indexed).
        deg (bool): If True, returns value in degrees. Defaults to True.

    Returns:
        np.ndarray: Array of phase values.
    """
    s = data.get_s(to_port, from_port)
    phase = np.angle(s)
    return rad_to_deg(phase) if deg else phase


def to_insertion_loss(data: TouchstoneData) -> np.ndarray:
    """
    Get Insertion Loss (|S21| in dB) as a positive value.

    Args:
        data (TouchstoneData): The Touchstone data.

    Returns:
        np.ndarray: Array of insertion loss values in dB.
    """
    if data.n_ports < 2:
        raise ValueError("Insertion loss requires at least 2 ports.")
    return -get_magnitude(data, 2, 1, db=True)


def to_return_loss(data: TouchstoneData) -> np.ndarray:
    """
    Get Return Loss (|S11| in dB) as a positive value.

    Args:
        data (TouchstoneData): The Touchstone data.

    Returns:
        np.ndarray: Array of return loss values in dB.
    """
    return -get_magnitude(data, 1, 1, db=True)


def to_vswr(data: TouchstoneData) -> np.ndarray:
    """
    Get VSWR calculated from S11.

    Args:
        data (TouchstoneData): The Touchstone data.

    Returns:
        np.ndarray: Array of VSWR values.
    """
    from .network_parameter_extensions import vswr_from_s11

    s11 = data.get_s(1, 1)
    return vswr_from_s11(s11)


def in_frequency_range(
    data: TouchstoneData, min_hz: float, max_hz: float
) -> TouchstoneData:
    """
    Filter data to a specific frequency range in Hz.

    Args:
        data (TouchstoneData): The original Touchstone data.
        min_hz (float): Minimum frequency in Hz.
        max_hz (float): Maximum frequency in Hz.

    Returns:
        TouchstoneData: A new filtered TouchstoneData instance.
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
    """Get an iterable of (FrequencyHz, NetworkParameter) for S11."""
    return data.get_parameter(1, 1)


def get_s21(data: TouchstoneData):
    """Get an iterable of (FrequencyHz, NetworkParameter) for S21."""
    return data.get_parameter(2, 1)


def get_s12(data: TouchstoneData):
    """Get an iterable of (FrequencyHz, NetworkParameter) for S12."""
    return data.get_parameter(1, 2)


def get_s22(data: TouchstoneData):
    """Get an iterable of (FrequencyHz, NetworkParameter) for S22."""
    return data.get_parameter(2, 2)


def get_frequencies_in(data: TouchstoneData, unit) -> np.ndarray:
    """Get all frequencies converted to the specified unit."""
    from .frequency_converter import get_multiplier

    return data.frequency / get_multiplier(unit)


def min_frequency_hz(data: TouchstoneData) -> float:
    """Get the minimum frequency in Hz."""
    if data.n_freq == 0:
        raise ValueError("Touchstone data contains no frequency points.")
    return float(np.min(data.frequency))


def max_frequency_hz(data: TouchstoneData) -> float:
    """Get the maximum frequency in Hz."""
    if data.n_freq == 0:
        raise ValueError("Touchstone data contains no frequency points.")
    return float(np.max(data.frequency))

