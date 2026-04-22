"""
NetworkParameter class representing a single complex S-parameter.
"""

import math
from dataclasses import dataclass
from typing import Any, Union


@dataclass(frozen=True)
class NetworkParameter:
    """
    A single network parameter (e.g., S11) represented as a complex number.
    """

    value: complex

    @property
    def real(self) -> float:
        """The real component of the parameter."""
        return self.value.real

    @property
    def imaginary(self) -> float:
        """The imaginary component of the parameter."""
        return self.value.imag

    @property
    def magnitude(self) -> float:
        """The linear magnitude of the parameter."""
        return abs(self.value)

    @property
    def magnitude_db(self) -> float:
        """The magnitude of the parameter in decibels (dB)."""
        mag = self.magnitude
        if mag == 0.0:
            return float("-inf")
        return 20.0 * math.log10(mag)

    @property
    def phase_radians(self) -> float:
        """The phase angle in radians."""
        from cmath import phase

        return phase(self.value)

    @property
    def phase_degrees(self) -> float:
        """The phase angle in degrees."""
        return math.degrees(self.phase_radians)

    @classmethod
    def from_real_imaginary(cls, real: float, imaginary: float) -> "NetworkParameter":
        """Create from real and imaginary parts."""
        return cls(complex(real, imaginary))

    @classmethod
    def from_magnitude_angle(
        cls, magnitude: float, angle_degrees: float
    ) -> "NetworkParameter":
        """Create from linear magnitude and angle in degrees."""
        import cmath

        rad = math.radians(angle_degrees)
        return cls(cmath.rect(magnitude, rad))

    @classmethod
    def from_decibel_angle(
        cls, magnitude_db: float, angle_degrees: float
    ) -> "NetworkParameter":
        """Create from magnitude in dB and angle in degrees."""
        magnitude = 10.0 ** (magnitude_db / 20.0)
        return cls.from_magnitude_angle(magnitude, angle_degrees)

    def conjugate(self) -> "NetworkParameter":
        """Return the complex conjugate of this parameter."""
        return NetworkParameter(self.value.conjugate())

    def reciprocal(self) -> "NetworkParameter":
        """Return the reciprocal (1 / x) of this parameter."""
        if self.value == 0j:
            raise ZeroDivisionError("Cannot compute the reciprocal of zero.")
        return NetworkParameter(1.0 / self.value)

    def __add__(
        self, other: Union["NetworkParameter", complex, float, int]
    ) -> "NetworkParameter":
        if isinstance(other, NetworkParameter):
            return NetworkParameter(self.value + other.value)
        return NetworkParameter(self.value + other)

    def __sub__(
        self, other: Union["NetworkParameter", complex, float, int]
    ) -> "NetworkParameter":
        if isinstance(other, NetworkParameter):
            return NetworkParameter(self.value - other.value)
        return NetworkParameter(self.value - other)

    def __mul__(
        self, other: Union["NetworkParameter", complex, float, int]
    ) -> "NetworkParameter":
        if isinstance(other, NetworkParameter):
            return NetworkParameter(self.value * other.value)
        return NetworkParameter(self.value * other)

    def __truediv__(
        self, other: Union["NetworkParameter", complex, float, int]
    ) -> "NetworkParameter":
        if isinstance(other, NetworkParameter):
            return NetworkParameter(self.value / other.value)
        return NetworkParameter(self.value / other)

    def approximately_equals(
        self, other: "NetworkParameter", tolerance: float = 1e-9
    ) -> bool:
        """Check if two parameters are approximately equal within a tolerance."""
        return abs(self.value - other.value) <= tolerance

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, NetworkParameter):
            return self.value == other.value
        return False
