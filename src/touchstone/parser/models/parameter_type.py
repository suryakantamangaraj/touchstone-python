"""
Network parameter types supported by Touchstone files.

Touchstone files can contain different types of network parameters.
This module defines the :class:`ParameterType` enumeration for the
five standard types specified in the Touchstone format.
"""

from enum import Enum


class ParameterType(Enum):
    """Enum representing the network parameter type.

    The parameter type is specified on the option line and determines
    how the data values are interpreted.

    Attributes:
        S: Scattering parameters (S-parameters).
        Y: Admittance parameters (Y-parameters).
        Z: Impedance parameters (Z-parameters).
        G: Hybrid-G parameters.
        H: Hybrid-H parameters.
    """

    S = "S"
    Y = "Y"
    Z = "Z"
    G = "G"
    H = "H"
