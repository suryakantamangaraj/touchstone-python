"""
Math utilities for network parameter conversions.

This module provides functions for converting between different
representations of RF network parameters: dB ↔ linear magnitude,
degrees ↔ radians, and various formats to complex numbers.
"""

from typing import Any

import numpy as np


def db_to_mag(db: Any) -> Any:
    """Convert decibels (dB) to linear magnitude.

    Computes ``10^(dB / 20)``.

    Args:
        db: The dB value(s). Can be a scalar, list, or NumPy array.

    Returns:
        The corresponding linear magnitude(s), same type as input.

    Example:
        >>> db_to_mag(-3)
        0.7079...
        >>> db_to_mag(0)
        1.0
    """
    return 10 ** (db / 20)


def mag_to_db(mag: Any) -> Any:
    """Convert linear magnitude to decibels (dB).

    Computes ``20 * log10(mag)``.

    Args:
        mag: The linear magnitude value(s). Must be positive.
            Can be a scalar, list, or NumPy array.

    Returns:
        The corresponding dB value(s), same type as input.

    Example:
        >>> mag_to_db(1.0)
        0.0
        >>> mag_to_db(0.5)
        -6.0206...
    """
    return 20 * np.log10(mag)


def deg_to_rad(deg: Any) -> Any:
    """Convert degrees to radians.

    Args:
        deg: Angle(s) in degrees. Can be a scalar, list, or NumPy array.

    Returns:
        Angle(s) in radians, same type as input.

    Example:
        >>> deg_to_rad(180)
        3.14159...
    """
    return np.deg2rad(deg)


def rad_to_deg(rad: Any) -> Any:
    """Convert radians to degrees.

    Args:
        rad: Angle(s) in radians. Can be a scalar, list, or NumPy array.

    Returns:
        Angle(s) in degrees, same type as input.

    Example:
        >>> import numpy as np
        >>> rad_to_deg(np.pi)
        180.0
    """
    return np.rad2deg(rad)


def ma_to_complex(mag: float, angle_deg: float) -> complex:
    """Convert magnitude and angle (degrees) to a complex number.

    Uses the formula: ``mag * (cos(θ) + j·sin(θ))`` where
    ``θ = radians(angle_deg)``.

    Args:
        mag: Linear magnitude (non-negative).
        angle_deg: Phase angle in degrees.

    Returns:
        complex: The complex number representation.

    Example:
        >>> ma_to_complex(1.0, 0.0)
        (1+0j)
    """
    angle_rad = deg_to_rad(angle_deg)
    return mag * (np.cos(angle_rad) + 1j * np.sin(angle_rad))


def db_to_complex(db: float, angle_deg: float) -> complex:
    """Convert magnitude (dB) and angle (degrees) to a complex number.

    First converts dB to linear magnitude, then delegates to
    :func:`ma_to_complex`.

    Args:
        db: Magnitude in decibels.
        angle_deg: Phase angle in degrees.

    Returns:
        complex: The complex number representation.

    Example:
        >>> db_to_complex(0.0, 0.0)
        (1+0j)
    """
    mag = db_to_mag(db)
    return ma_to_complex(mag, angle_deg)


def ri_to_complex(real: float, imag: float) -> complex:
    """Convert real and imaginary parts to a complex number.

    Args:
        real: The real part.
        imag: The imaginary part.

    Returns:
        complex: ``real + j*imag``.

    Example:
        >>> ri_to_complex(0.5, -0.3)
        (0.5-0.3j)
    """
    return complex(real, imag)


def vswr_from_s11(s11: Any) -> Any:
    """Calculate VSWR from the S11 reflection coefficient.

    Computes ``(1 + |S11|) / (1 - |S11|)``, with a small epsilon
    to avoid division by zero when ``|S11| ≈ 1``.

    Args:
        s11: Complex reflection coefficient value(s).
            Can be a scalar, list, or NumPy array.

    Returns:
        VSWR value(s), dimensionless and ≥ 1.0.

    Example:
        >>> vswr_from_s11(0.0)
        1.0
        >>> vswr_from_s11(0.5)
        3.0
    """
    mag = np.abs(s11)
    # Avoid division by zero by setting a small epsilon
    return (1 + mag) / np.maximum(1 - mag, 1e-10)
