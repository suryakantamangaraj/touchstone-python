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


def to_insertion_loss(data: TouchstoneData) -> np.ndarray:
    """Get Insertion Loss (|S21| in dB) as a positive value."""
    if data.n_ports < 2:
        raise ValueError("Insertion loss requires at least 2 ports.")
    return -get_magnitude(data, 2, 1, db=True)


def to_return_loss(data: TouchstoneData) -> np.ndarray:
    """Get Return Loss (|S11| in dB) as a positive value."""
    return -get_magnitude(data, 1, 1, db=True)


def to_vswr(data: TouchstoneData) -> np.ndarray:
    """Get VSWR calculated from S11."""
    from .network_parameter_extensions import vswr_from_s11

    s11 = data.get_s(1, 1)
    return vswr_from_s11(s11)


def in_frequency_range(
    data: TouchstoneData, min_hz: float, max_hz: float
) -> TouchstoneData:
    """Filter data to a specific frequency range in Hz."""
    mask = (data.frequency >= min_hz) & (data.frequency <= max_hz)
    return TouchstoneData(
        frequency=data.frequency[mask],
        s_parameters=data.s_parameters[mask],
        options=data.options,
        comments=data.comments,
        filename=data.filename,
        metadata=data.metadata,
    )
