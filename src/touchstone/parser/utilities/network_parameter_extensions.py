from typing import Any
import numpy as np

def db_to_mag(db: Any) -> Any:
    return 10 ** (db / 20)

def mag_to_db(mag: Any) -> Any:
    return 20 * np.log10(mag)

def deg_to_rad(deg: Any) -> Any:
    return np.deg2rad(deg)

def rad_to_deg(rad: Any) -> Any:
    return np.rad2deg(rad)

def ma_to_complex(mag: float, angle_deg: float) -> complex:
    angle_rad = deg_to_rad(angle_deg)
    return mag * (np.cos(angle_rad) + 1j * np.sin(angle_rad))

def db_to_complex(db: float, angle_deg: float) -> complex:
    mag = db_to_mag(db)
    return ma_to_complex(mag, angle_deg)

def ri_to_complex(real: float, imag: float) -> complex:
    return complex(real, imag)
