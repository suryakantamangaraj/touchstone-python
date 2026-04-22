import numpy as np
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from .touchstone_options import TouchstoneOptions

@dataclass(frozen=True)
class TouchstoneData:
    """
    Structured object representing Touchstone (.sNp) data.
    """
    frequency: np.ndarray  # 1D array of frequencies in Hz
    s_parameters: np.ndarray  # 3D array: (n_freq, n_ports, n_ports)
    options: TouchstoneOptions = field(default_factory=TouchstoneOptions)
    comments: List[str] = field(default_factory=list)
    filename: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    # Backward compatibility properties
    @property
    def z0(self) -> float:
        return self.options.reference_impedance

    @property
    def unit(self) -> str:
        return self.options.frequency_unit.value

    @property
    def parameter(self) -> str:
        return self.options.parameter_type.value

    @property
    def format(self) -> str:
        return self.options.data_format.value

    @property
    def n_ports(self) -> int:
        return self.s_parameters.shape[1]

    @property
    def n_freq(self) -> int:
        return len(self.frequency)

    def __post_init__(self):
        if self.s_parameters.shape[0] != self.n_freq:
            raise ValueError(
                f"Frequency length ({self.n_freq}) must match S-parameter length ({self.s_parameters.shape[0]})"
            )

    def get_s(self, to_port: int, from_port: int) -> np.ndarray:
        if not (1 <= to_port <= self.n_ports and 1 <= from_port <= self.n_ports):
            raise IndexError(f"Port indices out of range [1, {self.n_ports}]")
        return self.s_parameters[:, to_port - 1, from_port - 1]

    def __repr__(self) -> str:
        file_info = f", file: {self.filename}" if self.filename else ""
        return (
            f"TouchstoneData(n_ports={self.n_ports}, n_freq={self.n_freq}, "
            f"range=[{self.frequency[0]:.2e}, {self.frequency[-1]:.2e}] Hz{file_info})"
        )
