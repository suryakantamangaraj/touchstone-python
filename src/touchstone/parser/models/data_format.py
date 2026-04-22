"""
Data formats supported by Touchstone files.
"""

from enum import Enum


class DataFormat(Enum):
    """
    Enum representing the data format of the network parameters.
    """

    RI = "RI"  # Real/Imaginary
    MA = "MA"  # Magnitude/Angle
    DB = "DB"  # Decibel/Angle
