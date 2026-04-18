from typing import Any, Tuple

import numpy as np


def db_to_mag(db: Any) -> Any:
    """Convert dB to linear magnitude."""
    return 10 ** (db / 20)


def mag_to_db(mag: Any) -> Any:
    """Convert linear magnitude to dB."""
    return 20 * np.log10(mag)


def deg_to_rad(deg: Any) -> Any:
    """Convert degrees to radians."""
    return np.deg2rad(deg)


def rad_to_deg(rad: Any) -> Any:
    """Convert radians to degrees."""
    return np.rad2deg(rad)


def ma_to_complex(mag: float, angle_deg: float) -> complex:
    """Convert Magnitude/Angle (degrees) to complex number."""
    angle_rad = deg_to_rad(angle_deg)
    return mag * (np.cos(angle_rad) + 1j * np.sin(angle_rad))


def db_to_complex(db: float, angle_deg: float) -> complex:
    """Convert dB/Angle (degrees) to complex number."""
    mag = db_to_mag(db)
    return ma_to_complex(mag, angle_deg)


def ri_to_complex(real: float, imag: float) -> complex:
    """Convert Real/Imaginary to complex number."""
    return complex(real, imag)


def normalize_frequency(freq: float, unit: str) -> float:
    """Normalize frequency to Hz."""
    units = {"HZ": 1, "KHZ": 1e3, "MHZ": 1e6, "GHZ": 1e9}
    return freq * units.get(unit.upper(), 1)
