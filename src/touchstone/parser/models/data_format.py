"""
Data formats supported by Touchstone files.

Touchstone files can represent network parameter data in three different
numerical formats. This module defines the :class:`DataFormat` enumeration
used to distinguish between them.
"""

from enum import Enum


class DataFormat(Enum):
    """Enum representing the data format of the network parameters.

    Each Touchstone file specifies how parameter values are encoded in its
    option line. The three supported formats are:

    Attributes:
        RI: Real/Imaginary — parameters stored as ``(real, imaginary)`` pairs.
        MA: Magnitude/Angle — parameters stored as ``(linear_magnitude, angle_degrees)`` pairs.
        DB: Decibel/Angle — parameters stored as ``(magnitude_dB, angle_degrees)`` pairs.
    """

    RI = "RI"
    MA = "MA"
    DB = "DB"
