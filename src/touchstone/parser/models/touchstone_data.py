"""
Data model for Touchstone parsed data.

This module contains the :class:`TouchstoneData` dataclass, the primary
container for all data parsed from a Touchstone (``.sNp``) file. It holds
frequency arrays, S-parameter matrices, option line configuration,
comments, and metadata.
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
    """Structured object representing parsed Touchstone (.sNp) data.

    This is the main output of :meth:`TouchstoneParser.parse` and
    :meth:`TouchstoneParser.parse_string`. It is an immutable (frozen)
    dataclass that provides rich access to the underlying data.

    Attributes:
        frequency: 1-D NumPy array of frequency values in Hz.
        s_parameters: 3-D complex NumPy array of shape
            ``(n_freq, n_ports, n_ports)``.
        options: The parsed option line configuration.
        comments: List of comment strings extracted from the file.
        filename: The original filename, if known.
        metadata: Arbitrary metadata dictionary for user extensions.

    Example:
        >>> data = TouchstoneParser.parse("filter.s2p")
        >>> data.n_ports
        2
        >>> data.n_freq
        201
        >>> s21 = data.get_s(2, 1)
    """

    frequency: np.ndarray
    s_parameters: np.ndarray
    options: TouchstoneOptions = field(default_factory=TouchstoneOptions)
    comments: List[str] = field(default_factory=list)
    filename: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    # Backward compatibility properties
    @property
    def z0(self) -> float:
        """Reference impedance of the network in ohms.

        Returns:
            float: The reference impedance from the option line.
        """
        return self.options.reference_impedance

    @property
    def unit(self) -> str:
        """Frequency unit string (e.g. ``'Hz'``, ``'GHz'``).

        Returns:
            str: The frequency unit value from the option line.
        """
        return self.options.frequency_unit.value

    @property
    def parameter(self) -> str:
        """Network parameter type string (e.g. ``'S'``, ``'Y'``).

        Returns:
            str: The parameter type value from the option line.
        """
        return self.options.parameter_type.value

    @property
    def format(self) -> str:
        """Data format string (e.g. ``'MA'``, ``'RI'``).

        Returns:
            str: The data format value from the option line.
        """
        return self.options.data_format.value

    @property
    def n_ports(self) -> int:
        """Number of ports in the network.

        Returns:
            int: The number of ports, derived from the S-parameter matrix shape.
        """
        return self.s_parameters.shape[1]

    @property
    def n_freq(self) -> int:
        """Number of frequency points in the dataset.

        Returns:
            int: The length of the frequency array.
        """
        return len(self.frequency)

    @property
    def frequencies(self) -> np.ndarray:
        """Alias for :attr:`frequency` (compatibility with .NET API).

        Returns:
            numpy.ndarray: The frequency array in Hz.
        """
        return self.frequency

    @property
    def count(self) -> int:
        """Alias for :attr:`n_freq` (compatibility with .NET API).

        Returns:
            int: The number of frequency points.
        """
        return self.n_freq

    def __post_init__(self):
        """Validate the data after initialization.

        Raises:
            ValueError: If any of the required fields are ``None``, if the
                number of ports is less than 1, or if the frequency and
                S-parameter array lengths do not match.
        """
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
        """Get a specific S-parameter array across all frequencies.

        Extracts the complex-valued parameter ``S[to_port, from_port]``
        for every frequency point.

        Args:
            to_port: The target (output) port number, **1-indexed**.
            from_port: The source (input) port number, **1-indexed**.

        Returns:
            numpy.ndarray: 1-D complex array of length :attr:`n_freq`.

        Raises:
            IndexError: If port indices are out of range ``[1, n_ports]``.

        Example:
            >>> s21 = data.get_s(to_port=2, from_port=1)
        """
        if not (1 <= to_port <= self.n_ports and 1 <= from_port <= self.n_ports):
            raise IndexError(f"Port indices out of range [1, {self.n_ports}]")
        return self.s_parameters[:, to_port - 1, from_port - 1]

    def __getitem__(self, index: int) -> "FrequencyPoint":
        """Access the :class:`FrequencyPoint` at the given index.

        Args:
            index: Zero-based index into the frequency array.

        Returns:
            FrequencyPoint: The frequency point containing the frequency
            value and the N × N S-parameter matrix at that index.
        """
        from .frequency_point import FrequencyPoint

        return FrequencyPoint(self.frequency[index], self.s_parameters[index])

    def get_parameter(
        self, row: int, col: int
    ) -> Iterable[Tuple[float, "NetworkParameter"]]:
        """Iterate over (frequency, NetworkParameter) pairs for a specific matrix entry.

        Args:
            row: The row index of the parameter matrix, **1-indexed**.
            col: The column index of the parameter matrix, **1-indexed**.

        Yields:
            tuple: A 2-tuple of ``(frequency_hz, NetworkParameter)`` for each
            frequency point.

        Raises:
            IndexError: If row or col is out of range ``[1, n_ports]``.
        """
        from .network_parameter import NetworkParameter

        if not (1 <= row <= self.n_ports and 1 <= col <= self.n_ports):
            raise IndexError(f"Indices out of range [1, {self.n_ports}]")

        for f, s in zip(self.frequency, self.s_parameters[:, row - 1, col - 1]):
            yield (f, NetworkParameter(s))

    def where(self, predicate: Callable[["FrequencyPoint"], bool]) -> "TouchstoneData":
        """Filter the data using a predicate function.

        Creates a new :class:`TouchstoneData` containing only the frequency
        points for which the predicate returns ``True``.

        Args:
            predicate: A callable that takes a :class:`FrequencyPoint`
                and returns ``True`` to keep it.

        Returns:
            TouchstoneData: A new filtered instance.

        Example:
            >>> import numpy as np
            >>> filtered = data.where(lambda pt: np.abs(pt[0, 0].value) < 0.5)
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
        """Calculate insertion loss from S21.

        Insertion loss is computed as ``-|S21|`` in dB (positive values
        indicate loss).

        Returns:
            numpy.ndarray: Array of insertion loss values in dB.

        Raises:
            ValueError: If the network has fewer than 2 ports.
        """
        from ..utilities.touchstone_data_extensions import to_insertion_loss as _il

        return _il(self)

    def to_return_loss(self) -> np.ndarray:
        """Calculate return loss from S11.

        Return loss is computed as ``-|S11|`` in dB (positive values
        indicate better matching).

        Returns:
            numpy.ndarray: Array of return loss values in dB.
        """
        from ..utilities.touchstone_data_extensions import to_return_loss as _rl

        return _rl(self)

    def to_vswr(self) -> np.ndarray:
        """Calculate VSWR (Voltage Standing Wave Ratio) from S11.

        VSWR is computed as ``(1 + |S11|) / (1 - |S11|)``.

        Returns:
            numpy.ndarray: Array of VSWR values (dimensionless, ≥ 1.0).
        """
        from ..utilities.touchstone_data_extensions import to_vswr as _vswr

        return _vswr(self)

    def in_frequency_range(self, min_hz: float, max_hz: float) -> "TouchstoneData":
        """Filter the data to a specific frequency range.

        Args:
            min_hz: Minimum frequency in Hz (inclusive).
            max_hz: Maximum frequency in Hz (inclusive).

        Returns:
            TouchstoneData: A new instance containing only the points
            within the specified range.

        Example:
            >>> passband = data.in_frequency_range(2.0e9, 3.0e9)
        """
        from ..utilities.touchstone_data_extensions import in_frequency_range as _ifr

        return _ifr(self, min_hz, max_hz)

    def to_csv_string(
        self,
        format: Optional["DataFormat"] = None,
        unit: Optional["FrequencyUnit"] = None,
    ) -> str:
        """Export the data to a CSV formatted string.

        Args:
            format: Optional :class:`DataFormat` to override the default.
                If ``None``, uses the format from :attr:`options`.
            unit: Optional :class:`FrequencyUnit` to override the default.
                If ``None``, uses the unit from :attr:`options`.

        Returns:
            str: The CSV string representation of the data.
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
        """Write the data to a CSV file-like object or filepath.

        Args:
            writer: A file path (``str``) or a writable file-like object.
            format: Optional :class:`DataFormat` to override the default.
            unit: Optional :class:`FrequencyUnit` to override the default.
        """
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
        """Internal method to write CSV data to a file object.

        Args:
            file_obj: A writable file-like object.
            fmt: Optional data format override.
            unit: Optional frequency unit override.
        """
        import csv

        from ..utilities.frequency_converter import get_multiplier
        from .data_format import DataFormat

        writer = csv.writer(file_obj)

        actual_fmt = fmt if fmt is not None else self.options.data_format
        actual_unit = unit if unit is not None else self.options.frequency_unit

        headers = [f"Frequency ({actual_unit.value})"]
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
        """Return a developer-friendly string representation.

        Returns:
            str: A string showing the number of ports, frequency points,
            and frequency range.
        """
        file_info = f", file: {self.filename}" if self.filename else ""
        return (
            f"TouchstoneData(n_ports={self.n_ports}, n_freq={self.n_freq}, "
            f"range=[{self.frequency[0]:.2e}, {self.frequency[-1]:.2e}] Hz{file_info})"
        )
