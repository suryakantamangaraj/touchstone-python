"""
Utility for frequency conversions.
"""

def normalize_frequency(freq: float, unit: str) -> float:
    """
    Normalize frequency to Hz.
    
    Args:
        freq (float): The frequency value.
        unit (str): The frequency unit (e.g., 'Hz', 'kHz').
        
    Returns:
        float: The frequency in Hz.
    """
    units = {"HZ": 1, "KHZ": 1e3, "MHZ": 1e6, "GHZ": 1e9}
    return freq * units.get(unit.upper(), 1)
