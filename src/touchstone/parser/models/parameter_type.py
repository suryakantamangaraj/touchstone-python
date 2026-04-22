"""
Network parameter types supported by Touchstone files.
"""

from enum import Enum


class ParameterType(Enum):
    """
    Enum representing the network parameter type.
    """
    S = "S"
    Y = "Y"
    Z = "Z"
    G = "G"
    H = "H"
