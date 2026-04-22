"""
Data model for Touchstone parsed data.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

import numpy as np

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
        """Reference impedance of the network."""
        return self.options.reference_impedance

    @property
    def unit(self) -> str:
        """Frequency unit (e.g. 'Hz', 'GHz')."""
        return self.options.frequency_unit.value

    @property
    def parameter(self) -> str:
        """Network parameter type (e.g. 'S', 'Y')."""
        return self.options.parameter_type.value

    @property
    def format(self) -> str:
        """Data format (e.g. 'MA', 'RI')."""
        return self.options.data_format.value

    @property
    def n_ports(self) -> int:
        """Number of ports in the network."""
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
        Get the specific S-parameter (or Y, Z) array across all frequencies.

        Args:
            to_port (int): The target port (1-indexed).
            from_port (int): The source port (1-indexed).

        Returns:
            np.ndarray: Complex array of the parameter values.
        """
        if not (1 <= to_port <= self.n_ports and 1 <= from_port <= self.n_ports):
            raise IndexError(f"Port indices out of range [1, {self.n_ports}]")
        return self.s_parameters[:, to_port - 1, from_port - 1]

    def to_insertion_loss(self) -> np.ndarray:
        """
        Calculate insertion loss (positive dB) from S21.

        Returns:
            np.ndarray: Array of insertion loss values in dB.
        """
        from ..utilities.touchstone_data_extensions import to_insertion_loss as _il

        return _il(self)

    def to_return_loss(self) -> np.ndarray:
        """
        Calculate return loss (positive dB) from S11.

        Returns:
            np.ndarray: Array of return loss values in dB.
        """
        from ..utilities.touchstone_data_extensions import to_return_loss as _rl

        return _rl(self)

    def to_vswr(self) -> np.ndarray:
        """
        Calculate VSWR from S11.

        Returns:
            np.ndarray: Array of VSWR values.
        """
        from ..utilities.touchstone_data_extensions import to_vswr as _vswr

        return _vswr(self)

    def in_frequency_range(self, min_hz: float, max_hz: float) -> "TouchstoneData":
        """
        Filter the data to a specific frequency range.

        Args:
            min_hz (float): Minimum frequency in Hz.
            max_hz (float): Maximum frequency in Hz.

        Returns:
            TouchstoneData: A new filtered instance.
        """
        from ..utilities.touchstone_data_extensions import in_frequency_range as _ifr

        return _ifr(self, min_hz, max_hz)

    def to_csv_string(self) -> str:
        """
        Export the data to a CSV formatted string.

        Returns:
            str: CSV string representation.
        """
        import io

        output = io.StringIO()
        self.to_csv(output)
        return output.getvalue()

    def to_csv(self, writer: Any) -> None:
        """Writes the data to a CSV file-like object or filepath."""
        import csv

        # If writer is a string, open it as a file
        if isinstance(writer, str):
            with open(writer, "w", newline="", encoding="utf-8") as f:
                self._write_csv(f)
        else:
            self._write_csv(writer)

    def _write_csv(self, file_obj: Any) -> None:
        import csv

        writer = csv.writer(file_obj)

        headers = ["Frequency (Hz)"]
        for i in range(1, self.n_ports + 1):
            for j in range(1, self.n_ports + 1):
                headers.extend([f"S{i}{j}_Mag", f"S{i}{j}_Phase(deg)"])
        writer.writerow(headers)

        for p in range(self.n_freq):
            row = [self.frequency[p]]
            for i in range(self.n_ports):
                for j in range(self.n_ports):
                    s = self.s_parameters[p, i, j]
                    row.extend([np.abs(s), np.angle(s, deg=True)])
            writer.writerow(row)

    def __repr__(self) -> str:
        file_info = f", file: {self.filename}" if self.filename else ""
        return (
            f"TouchstoneData(n_ports={self.n_ports}, n_freq={self.n_freq}, "
            f"range=[{self.frequency[0]:.2e}, {self.frequency[-1]:.2e}] Hz{file_info})"
        )
