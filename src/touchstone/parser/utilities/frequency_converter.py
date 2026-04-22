from typing import Any
import numpy as np


def normalize_frequency(freq: float, unit: str) -> float:
    """Normalize frequency to Hz."""
    units = {"HZ": 1, "KHZ": 1e3, "MHZ": 1e6, "GHZ": 1e9}
    return freq * units.get(unit.upper(), 1)
