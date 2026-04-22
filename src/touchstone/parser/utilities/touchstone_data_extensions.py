import numpy as np
from ..models.touchstone_data import TouchstoneData
from .network_parameter_extensions import mag_to_db, rad_to_deg


def get_magnitude(
    data: TouchstoneData, to_port: int, from_port: int, db: bool = True
) -> np.ndarray:
    """Get magnitude of S-parameters (defaults to dB)."""
    s = data.get_s(to_port, from_port)
    mag = np.abs(s)
    return mag_to_db(mag) if db else mag


def get_phase(
    data: TouchstoneData, to_port: int, from_port: int, deg: bool = True
) -> np.ndarray:
    """Get phase of S-parameters (defaults to degrees)."""
    s = data.get_s(to_port, from_port)
    phase = np.angle(s)
    return rad_to_deg(phase) if deg else phase
