"""
Math utilities for network parameter conversions.
"""

from typing import Any

import numpy as np


def db_to_mag(db: Any) -> Any:
    """
    Convert Decibels (dB) to linear magnitude.
    
    Args:
        db (Any): The dB value(s).
        
    Returns:
        Any: Linear magnitude.
    """
    return 10 ** (db / 20)


def mag_to_db(mag: Any) -> Any:
    """
    Convert linear magnitude to Decibels (dB).
    
    Args:
        mag (Any): The linear magnitude.
        
    Returns:
        Any: Magnitude in dB.
    """
    return 20 * np.log10(mag)


def deg_to_rad(deg: Any) -> Any:
    """
    Convert degrees to radians.
    
    Args:
        deg (Any): Angle in degrees.
        
    Returns:
        Any: Angle in radians.
    """
    return np.deg2rad(deg)


def rad_to_deg(rad: Any) -> Any:
    """
    Convert radians to degrees.
    
    Args:
        rad (Any): Angle in radians.
        
    Returns:
        Any: Angle in degrees.
    """
    return np.rad2deg(rad)


def ma_to_complex(mag: float, angle_deg: float) -> complex:
    """
    Convert magnitude and angle (degrees) to a complex number.
    
    Args:
        mag (float): Linear magnitude.
        angle_deg (float): Phase angle in degrees.
        
    Returns:
        complex: The complex number representation.
    """
    angle_rad = deg_to_rad(angle_deg)
    return mag * (np.cos(angle_rad) + 1j * np.sin(angle_rad))


def db_to_complex(db: float, angle_deg: float) -> complex:
    """
    Convert magnitude (dB) and angle (degrees) to a complex number.
    
    Args:
        db (float): Magnitude in decibels.
        angle_deg (float): Phase angle in degrees.
        
    Returns:
        complex: The complex number representation.
    """
    mag = db_to_mag(db)
    return ma_to_complex(mag, angle_deg)


def ri_to_complex(real: float, imag: float) -> complex:
    """
    Convert real and imaginary parts to a complex number.
    
    Args:
        real (float): Real part.
        imag (float): Imaginary part.
        
    Returns:
        complex: The complex number.
    """
    return complex(real, imag)


def vswr_from_s11(s11: Any) -> Any:
    """
    Calculate VSWR from S11 parameter.
    
    Args:
        s11 (Any): Complex reflection coefficient.
        
    Returns:
        Any: Voltage Standing Wave Ratio.
    """
    mag = np.abs(s11)
    # Avoid division by zero by setting a small epsilon
    return (1 + mag) / np.maximum(1 - mag, 1e-10)
