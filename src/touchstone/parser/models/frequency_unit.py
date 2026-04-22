"""
Frequency units supported by Touchstone files.
"""

from enum import Enum


class FrequencyUnit(Enum):
    """
    Enum representing the frequency unit.
    """

    HZ = "Hz"
    KHZ = "kHz"
    MHZ = "MHz"
    GHZ = "GHz"
