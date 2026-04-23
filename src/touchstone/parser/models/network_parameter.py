"""
NetworkParameter class representing a single complex S-parameter.

This module defines the :class:`NetworkParameter` dataclass, which wraps
a single complex number and provides convenient access to its magnitude,
phase, and dB representation. It also supports arithmetic operations and
factory methods for creating parameters from different formats.
"""

import math
from dataclasses import dataclass
from typing import Any, Union


@dataclass(frozen=True)
class NetworkParameter:
    """A single network parameter (e.g., S11) represented as a complex number.

    This immutable dataclass provides rich access to the underlying complex
    value, including magnitude (linear and dB), phase (radians and degrees),
    real/imaginary decomposition, and arithmetic operators.

    Attributes:
        value: The complex-valued network parameter.

    Example:
        >>> param = NetworkParameter(complex(0.5, -0.3))
        >>> param.magnitude_db
        -4.86...
        >>> param.phase_degrees
        -30.96...
    """

    value: complex

    @property
    def real(self) -> float:
        """The real component of the parameter.

        Returns:
            float: The real part of the complex value.
        """
        return self.value.real

    @property
    def imaginary(self) -> float:
        """The imaginary component of the parameter.

        Returns:
            float: The imaginary part of the complex value.
        """
        return self.value.imag

    @property
    def magnitude(self) -> float:
        """The linear magnitude (absolute value) of the parameter.

        Returns:
            float: ``|value|``, always non-negative.
        """
        return abs(self.value)

    @property
    def magnitude_db(self) -> float:
        """The magnitude of the parameter in decibels (dB).

        Computed as ``20 * log10(|value|)``.

        Returns:
            float: Magnitude in dB. Returns ``-inf`` if magnitude is zero.
        """
        mag = self.magnitude
        if mag == 0.0:
            return float("-inf")
        return 20.0 * math.log10(mag)

    @property
    def phase_radians(self) -> float:
        """The phase angle in radians.

        Returns:
            float: Phase angle in the range ``(-π, π]``.
        """
        from cmath import phase

        return phase(self.value)

    @property
    def phase_degrees(self) -> float:
        """The phase angle in degrees.

        Returns:
            float: Phase angle in the range ``(-180, 180]``.
        """
        return math.degrees(self.phase_radians)

    @classmethod
    def from_real_imaginary(cls, real: float, imaginary: float) -> "NetworkParameter":
        """Create a NetworkParameter from real and imaginary parts.

        Args:
            real: The real component.
            imaginary: The imaginary component.

        Returns:
            NetworkParameter: A new instance with ``value = real + j*imaginary``.
        """
        return cls(complex(real, imaginary))

    @classmethod
    def from_magnitude_angle(
        cls, magnitude: float, angle_degrees: float
    ) -> "NetworkParameter":
        """Create a NetworkParameter from linear magnitude and angle.

        Args:
            magnitude: The linear magnitude (non-negative).
            angle_degrees: The phase angle in degrees.

        Returns:
            NetworkParameter: A new instance created via polar-to-rectangular
            conversion.
        """
        import cmath

        rad = math.radians(angle_degrees)
        return cls(cmath.rect(magnitude, rad))

    @classmethod
    def from_decibel_angle(
        cls, magnitude_db: float, angle_degrees: float
    ) -> "NetworkParameter":
        """Create a NetworkParameter from magnitude in dB and angle.

        First converts dB to linear magnitude, then delegates to
        :meth:`from_magnitude_angle`.

        Args:
            magnitude_db: The magnitude in decibels.
            angle_degrees: The phase angle in degrees.

        Returns:
            NetworkParameter: A new instance.
        """
        magnitude = 10.0 ** (magnitude_db / 20.0)
        return cls.from_magnitude_angle(magnitude, angle_degrees)

    def conjugate(self) -> "NetworkParameter":
        """Return the complex conjugate of this parameter.

        Returns:
            NetworkParameter: A new instance with the conjugated value.
        """
        return NetworkParameter(self.value.conjugate())

    def reciprocal(self) -> "NetworkParameter":
        """Return the reciprocal (``1 / value``) of this parameter.

        Returns:
            NetworkParameter: A new instance with the reciprocal value.

        Raises:
            ZeroDivisionError: If the value is zero.
        """
        if self.value == 0j:
            raise ZeroDivisionError("Cannot compute the reciprocal of zero.")
        return NetworkParameter(1.0 / self.value)

    def __add__(
        self, other: Union["NetworkParameter", complex, float, int]
    ) -> "NetworkParameter":
        """Add two parameters or a parameter and a scalar.

        Args:
            other: Another :class:`NetworkParameter`, complex, float, or int.

        Returns:
            NetworkParameter: The sum as a new instance.
        """
        if isinstance(other, NetworkParameter):
            return NetworkParameter(self.value + other.value)
        return NetworkParameter(self.value + other)

    def __sub__(
        self, other: Union["NetworkParameter", complex, float, int]
    ) -> "NetworkParameter":
        """Subtract a parameter or scalar from this parameter.

        Args:
            other: Another :class:`NetworkParameter`, complex, float, or int.

        Returns:
            NetworkParameter: The difference as a new instance.
        """
        if isinstance(other, NetworkParameter):
            return NetworkParameter(self.value - other.value)
        return NetworkParameter(self.value - other)

    def __mul__(
        self, other: Union["NetworkParameter", complex, float, int]
    ) -> "NetworkParameter":
        """Multiply this parameter by another parameter or scalar.

        Args:
            other: Another :class:`NetworkParameter`, complex, float, or int.

        Returns:
            NetworkParameter: The product as a new instance.
        """
        if isinstance(other, NetworkParameter):
            return NetworkParameter(self.value * other.value)
        return NetworkParameter(self.value * other)

    def __truediv__(
        self, other: Union["NetworkParameter", complex, float, int]
    ) -> "NetworkParameter":
        """Divide this parameter by another parameter or scalar.

        Args:
            other: Another :class:`NetworkParameter`, complex, float, or int.

        Returns:
            NetworkParameter: The quotient as a new instance.
        """
        if isinstance(other, NetworkParameter):
            return NetworkParameter(self.value / other.value)
        return NetworkParameter(self.value / other)

    def approximately_equals(
        self, other: "NetworkParameter", tolerance: float = 1e-9
    ) -> bool:
        """Check if two parameters are approximately equal.

        Args:
            other: The other :class:`NetworkParameter` to compare.
            tolerance: The maximum allowed absolute difference.
                Defaults to ``1e-9``.

        Returns:
            bool: ``True`` if ``|self.value - other.value| <= tolerance``.
        """
        return abs(self.value - other.value) <= tolerance

    def __eq__(self, other: Any) -> bool:
        """Check exact equality with another NetworkParameter.

        Args:
            other: The object to compare.

        Returns:
            bool: ``True`` if *other* is a :class:`NetworkParameter` with
            an identical complex value.
        """
        if isinstance(other, NetworkParameter):
            return self.value == other.value
        return False
