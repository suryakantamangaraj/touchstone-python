"""
Frequency units supported by Touchstone files.

The option line of a Touchstone file specifies the frequency unit used
for all data points. This module defines the :class:`FrequencyUnit`
enumeration for the four supported units.
"""

from enum import Enum


class FrequencyUnit(Enum):
    """Enum representing the frequency unit used in a Touchstone file.

    The frequency unit determines how raw frequency values in the data
    section are interpreted. All values are internally normalized to Hz
    during parsing.

    Attributes:
        HZ: Hertz (1 Hz).
        KHZ: Kilohertz (1 × 10³ Hz).
        MHZ: Megahertz (1 × 10⁶ Hz).
        GHZ: Gigahertz (1 × 10⁹ Hz).
    """

    HZ = "Hz"
    KHZ = "kHz"
    MHZ = "MHz"
    GHZ = "GHz"
