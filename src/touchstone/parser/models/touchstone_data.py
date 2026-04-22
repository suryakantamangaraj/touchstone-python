"""
Data model for Touchstone parsed data.
"""

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Callable, Dict, Iterable, List, Optional, Tuple

import numpy as np

from .touchstone_options import TouchstoneOptions

if TYPE_CHECKING:
    from .data_format import DataFormat
    from .frequency_point import FrequencyPoint
    from .frequency_unit import FrequencyUnit
    from .network_parameter import NetworkParameter


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

    @property
    def frequencies(self) -> np.ndarray:
        """Alias for frequency (compatibility with .NET)."""
        return self.frequency

    @property
    def count(self) -> int:
        """Alias for n_freq (compatibility with .NET)."""
        return self.n_freq

    def __post_init__(self):
        if self.options is None:
            raise ValueError("options cannot be None")
        if self.frequency is None:
            raise ValueError("frequency array cannot be None")
        if self.s_parameters is None:
            raise ValueError("s_parameters array cannot be None")
        if self.n_ports < 1:
            raise ValueError(f"Number of ports must be >= 1. Got {self.n_ports}")
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

    def __getitem__(self, index: int) -> "FrequencyPoint":
        """Access the FrequencyPoint at the given index."""
        from .frequency_point import FrequencyPoint

        return FrequencyPoint(self.frequency[index], self.s_parameters[index])

    def get_parameter(
        self, row: int, col: int
    ) -> Iterable[Tuple[float, "NetworkParameter"]]:
        """
        Get an iterable of (FrequencyHz, NetworkParameter) for the specific row and column (1-indexed).
        """
        from .network_parameter import NetworkParameter

        if not (1 <= row <= self.n_ports and 1 <= col <= self.n_ports):
            raise IndexError(f"Indices out of range [1, {self.n_ports}]")

        for f, s in zip(self.frequency, self.s_parameters[:, row - 1, col - 1]):
            yield (f, NetworkParameter(s))

    def where(self, predicate: Callable[["FrequencyPoint"], bool]) -> "TouchstoneData":
        """
        Filter the data using a predicate function on FrequencyPoint.

        Args:
            predicate: A function that takes a FrequencyPoint and returns True to keep it.

        Returns:
            TouchstoneData: A new filtered instance.
        """
        keep_indices = [i for i in range(self.n_freq) if predicate(self[i])]
        return TouchstoneData(
            frequency=self.frequency[keep_indices],
            s_parameters=self.s_parameters[keep_indices],
            options=self.options,
            comments=self.comments,
            filename=self.filename,
            metadata=self.metadata,
        )

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

    def to_csv_string(
        self,
        format: Optional["DataFormat"] = None,
        unit: Optional["FrequencyUnit"] = None,
    ) -> str:
        """
        Export the data to a CSV formatted string.

        Args:
            format: Optional DataFormat to override the default.
            unit: Optional FrequencyUnit to override the default.

        Returns:
            str: CSV string representation.
        """
        import io

        output = io.StringIO()
        self.to_csv(output, format=format, unit=unit)
        return output.getvalue()

    def to_csv(
        self,
        writer: Any,
        format: Optional["DataFormat"] = None,
        unit: Optional["FrequencyUnit"] = None,
    ) -> None:
        """Writes the data to a CSV file-like object or filepath."""
        # If writer is a string, open it as a file
        if isinstance(writer, str):
            with open(writer, "w", newline="", encoding="utf-8") as f:
                self._write_csv(f, format, unit)
        else:
            self._write_csv(writer, format, unit)

    def _write_csv(
        self,
        file_obj: Any,
        fmt: Optional["DataFormat"] = None,
        unit: Optional["FrequencyUnit"] = None,
    ) -> None:
        import csv

        from ..utilities.frequency_converter import get_multiplier
        from .data_format import DataFormat
        from .frequency_unit import FrequencyUnit

        writer = csv.writer(file_obj)

        actual_fmt = fmt if fmt is not None else self.options.data_format
        actual_unit = unit if unit is not None else self.options.frequency_unit

        headers = [f"Frequency ({actual_unit.name})"]
        for i in range(1, self.n_ports + 1):
            for j in range(1, self.n_ports + 1):
                if actual_fmt == DataFormat.RI:
                    headers.extend([f"S{i}{j}_Re", f"S{i}{j}_Im"])
                elif actual_fmt == DataFormat.DB:
                    headers.extend([f"S{i}{j}_dB", f"S{i}{j}_Phase(deg)"])
                else:
                    headers.extend([f"S{i}{j}_Mag", f"S{i}{j}_Phase(deg)"])
        writer.writerow(headers)

        for p in range(self.n_freq):
            f_val = self.frequency[p] / get_multiplier(actual_unit)

            row = [f_val]
            for i in range(self.n_ports):
                for j in range(self.n_ports):
                    s = self.s_parameters[p, i, j]
                    if actual_fmt == DataFormat.RI:
                        row.extend([s.real, s.imag])
                    elif actual_fmt == DataFormat.DB:
                        mag = np.abs(s)
                        db = 20 * np.log10(mag) if mag > 0 else float("-inf")
                        row.extend([db, np.angle(s, deg=True)])
                    else:
                        row.extend([np.abs(s), np.angle(s, deg=True)])
            writer.writerow(row)

    def __repr__(self) -> str:
        file_info = f", file: {self.filename}" if self.filename else ""
        return (
            f"TouchstoneData(n_ports={self.n_ports}, n_freq={self.n_freq}, "
            f"range=[{self.frequency[0]:.2e}, {self.frequency[-1]:.2e}] Hz{file_info})"
        )
