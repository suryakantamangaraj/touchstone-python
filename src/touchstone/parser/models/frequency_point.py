"""
FrequencyPoint class representing a single frequency point and its S-parameters.

A :class:`FrequencyPoint` encapsulates one row of a Touchstone dataset —
a single frequency value together with its N × N matrix of complex
network parameters.
"""

from dataclasses import dataclass

import numpy as np

from .network_parameter import NetworkParameter


@dataclass(frozen=True)
class FrequencyPoint:
    """Encapsulates a single frequency point and its N × N matrix of network parameters.

    Attributes:
        frequency_hz: The frequency value in Hz (must be non-negative).
        _s_parameters: The N × N complex NumPy array of S-parameters
            at this frequency.

    Raises:
        ValueError: If the frequency is negative or the S-parameter array
            is not a square matrix.

    Example:
        >>> point = data[0]  # first frequency point
        >>> point.frequency_hz
        1000000000.0
        >>> point.number_of_ports
        2
        >>> s11 = point[0, 0]
    """

    frequency_hz: float
    _s_parameters: np.ndarray

    def __post_init__(self):
        """Validate inputs after initialization.

        Raises:
            ValueError: If frequency is negative or S-parameters are not
                a square matrix.
        """
        if self.frequency_hz < 0:
            raise ValueError(f"Frequency cannot be negative. Got {self.frequency_hz}")
        if (
            self._s_parameters.ndim != 2
            or self._s_parameters.shape[0] != self._s_parameters.shape[1]
        ):
            raise ValueError(
                f"S-parameters must be a square matrix. Got shape {self._s_parameters.shape}"
            )

    @property
    def number_of_ports(self) -> int:
        """The number of ports (N for an N × N matrix).

        Returns:
            int: The dimension of the S-parameter matrix.
        """
        return self._s_parameters.shape[0]

    def get_parameter_matrix(self) -> np.ndarray:
        """Get a defensive copy of the complex S-parameter matrix.

        Returns a copy so that external code cannot mutate the
        internal state of this frozen dataclass.

        Returns:
            numpy.ndarray: An N × N complex array.
        """
        return self._s_parameters.copy()

    def __getitem__(self, indices: tuple[int, int]) -> NetworkParameter:
        """Access a specific network parameter by ``[row, col]`` index.

        Args:
            indices: A tuple of ``(row, col)`` indices, **0-indexed**.

        Returns:
            NetworkParameter: The network parameter at the specified index.

        Raises:
            IndexError: If indices are not a 2-tuple or are out of range.
        """
        if not isinstance(indices, tuple) or len(indices) != 2:
            raise IndexError("Indices must be a tuple of (row, col).")
        row, col = indices
        if not (0 <= row < self.number_of_ports and 0 <= col < self.number_of_ports):
            raise IndexError(
                f"Index [{row}, {col}] is out of range for {self.number_of_ports}-port data."
            )
        return NetworkParameter(self._s_parameters[row, col])

    def __str__(self) -> str:
        """Return a human-readable string representation.

        Returns:
            str: A string showing the frequency and port count.
        """
        return f"FrequencyPoint(freq={self.frequency_hz:.2e} Hz, ports={self.number_of_ports})"

    def __repr__(self) -> str:
        """Return a developer-friendly string representation.

        Returns:
            str: Same as :meth:`__str__`.
        """
        return self.__str__()
