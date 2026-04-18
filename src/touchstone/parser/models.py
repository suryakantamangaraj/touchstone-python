from dataclasses import dataclass, field
from typing import Any, Dict, Optional

import numpy as np


@dataclass(frozen=True)
class TouchstoneData:
    """
    Structured object representing Touchstone (.sNp) data.
    """

    frequency: np.ndarray  # 1D array of frequencies in Hz
    s_parameters: np.ndarray  # 3D array: (n_freq, n_ports, n_ports)
    z0: float = 50.0  # Reference impedance in Ohms
    unit: str = "Hz"
    parameter: str = "S"  # S, Y, Z, G, H
    format: str = "RI"  # RI, MA, DB
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def n_ports(self) -> int:
        """Number of ports in the data."""
        return self.s_parameters.shape[1]

    @property
    def n_freq(self) -> int:
        """Number of frequency points."""
        return len(self.frequency)

    def __post_init__(self):
        if self.s_parameters.shape[0] != self.n_freq:
            raise ValueError(
                f"Frequency length ({self.n_freq}) must match S-parameter length ({self.s_parameters.shape[0]})"
            )

    def get_s(self, to_port: int, from_port: int) -> np.ndarray:
        """
        Get S-parameters for a specific path (1-indexed).
        Example: data.get_s(2, 1) returns S21.
        """
        if not (1 <= to_port <= self.n_ports and 1 <= from_port <= self.n_ports):
            raise IndexError(f"Port indices out of range [1, {self.n_ports}]")
        return self.s_parameters[:, to_port - 1, from_port - 1]

    def magnitude(self, to_port: int, from_port: int, db: bool = True) -> np.ndarray:
        """Get magnitude of S-parameters (defaults to dB)."""
        from .utils import mag_to_db

        s = self.get_s(to_port, from_port)
        mag = np.abs(s)
        return mag_to_db(mag) if db else mag

    def phase(self, to_port: int, from_port: int, deg: bool = True) -> np.ndarray:
        """Get phase of S-parameters (defaults to degrees)."""
        from .utils import rad_to_deg

        s = self.get_s(to_port, from_port)
        phase = np.angle(s)
        return rad_to_deg(phase) if deg else phase

    def __repr__(self) -> str:
        return (
            f"TouchstoneData(n_ports={self.n_ports}, n_freq={self.n_freq}, "
            f"range=[{self.frequency[0]:.2e}, {self.frequency[-1]:.2e}] Hz)"
        )
