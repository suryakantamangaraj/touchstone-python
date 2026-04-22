"""
FrequencyPoint class representing a single frequency point and its S-parameters.
"""

from dataclasses import dataclass
from typing import Any, Tuple

import numpy as np

from .network_parameter import NetworkParameter


@dataclass(frozen=True)
class FrequencyPoint:
    """
    Encapsulates a single frequency point and its N x N matrix of network parameters.
    """

    frequency_hz: float
    _s_parameters: np.ndarray

    def __post_init__(self):
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
        """The number of ports (N for an N x N matrix)."""
        return self._s_parameters.shape[0]

    def get_parameter_matrix(self) -> np.ndarray:
        """
        Get a defensive copy of the complex S-parameter matrix for this frequency.

        Returns:
            np.ndarray: N x N complex array.
        """
        return self._s_parameters.copy()

    def __getitem__(self, indices: Tuple[int, int]) -> NetworkParameter:
        """
        Access a specific network parameter by [row, col] index (0-indexed).

        Args:
            indices (Tuple[int, int]): The (row, col) indices.

        Returns:
            NetworkParameter: The network parameter at the specified index.
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
        return f"FrequencyPoint(freq={self.frequency_hz:.2e} Hz, ports={self.number_of_ports})"

    def __repr__(self) -> str:
        return self.__str__()
