import re
from typing import Iterator, List, Optional, Tuple

import numpy as np

from .models import TouchstoneData
from .utils import db_to_complex, ma_to_complex, normalize_frequency, ri_to_complex


def _strip_comments(line: str) -> str:
    """Remove comments starting with '!'."""
    return line.split("!")[0].strip()


def _get_numbers(lines: Iterator[str]) -> Iterator[float]:
    """Yield all numbers found in the lines, ignoring comments."""
    for line in lines:
        clean_line = _strip_comments(line)
        if not clean_line or clean_line.startswith("#"):
            continue
        # Split by whitespace or comma
        parts = re.split(r"[\s,]+", clean_line)
        for part in parts:
            if part:
                try:
                    yield float(part)
                except ValueError:
                    continue


def read_snp(filepath: str) -> TouchstoneData:
    """
    Parse a Touchstone (.sNp) file.

    Args:
        filepath: Path to the .sNp file.

    Returns:
        TouchstoneData object containing frequencies and S-parameters.
    """
    # Detect n_ports from filename extension
    ext_match = re.search(r"\.s(\d+)p$", filepath.lower())
    if not ext_match:
        raise ValueError(f"Could not determine port count from extension of {filepath}")
    n_ports = int(ext_match.group(1))

    # Default options
    freq_unit = "GHZ"
    param_type = "S"
    data_format = "MA"
    z0 = 50.0

    # First pass: Parse option line and prepare for data extraction
    with open(filepath, "r") as f:
        for line in f:
            clean_line = _strip_comments(line)
            if clean_line.startswith("#"):
                parts = clean_line[1:].strip().split()
                # Format: # [Hz|kHz|MHz|GHz] [S|Y|Z|G|H] [DB|MA|RI] [R n]
                i = 0
                while i < len(parts):
                    part = parts[i].upper()
                    if part in ["HZ", "KHZ", "MHZ", "GHZ"]:
                        freq_unit = part
                    elif part in ["S", "Y", "Z", "G", "H"]:
                        param_type = part
                    elif part in ["DB", "MA", "RI"]:
                        data_format = part
                    elif part == "R":
                        if i + 1 < len(parts):
                            z0 = float(parts[i + 1])
                            i += 1
                    i += 1
                break

    # Second pass: Extract all data numbers efficiently
    with open(filepath, "r") as f:
        numbers = list(_get_numbers(f))

    # Each complex S-parameter is 2 numbers.
    # Each frequency point has 1 frequency and n_ports^2 * 2 numbers.
    nums_per_freq = 1 + (n_ports**2 * 2)
    if len(numbers) % nums_per_freq != 0:
        # Some files might have missing data or trailing numbers
        n_points = len(numbers) // nums_per_freq
        numbers = numbers[: n_points * nums_per_freq]
    else:
        n_points = len(numbers) // nums_per_freq

    data = np.array(numbers).reshape(n_points, nums_per_freq)

    freqs = np.array([normalize_frequency(f, freq_unit) for f in data[:, 0]])
    raw_s = data[:, 1:]

    # Reshape and convert to complex
    s_params = np.zeros((n_points, n_ports, n_ports), dtype=complex)

    def to_complex(v1, v2):
        if data_format == "RI":
            return ri_to_complex(v1, v2)
        elif data_format == "DB":
            return db_to_complex(v1, v2)
        else:
            return ma_to_complex(v1, v2)

    for p in range(n_points):
        row = raw_s[p]
        # Touchstone ordering:
        # 1-port: S11
        # 2-port: S11, S21, S12, S22 (Special case!)
        # N-port: S11, S12, ..., S1n, S21, ..., Snn

        if n_ports == 1:
            s_params[p, 0, 0] = to_complex(row[0], row[1])
        elif n_ports == 2:
            s_params[p, 0, 0] = to_complex(row[0], row[1])  # S11
            s_params[p, 1, 0] = to_complex(row[2], row[3])  # S21
            s_params[p, 0, 1] = to_complex(row[4], row[5])  # S12
            s_params[p, 1, 1] = to_complex(row[6], row[7])  # S22
        else:
            idx = 0
            for i in range(n_ports):
                for j in range(n_ports):
                    s_params[p, i, j] = to_complex(row[idx], row[idx + 1])
                    idx += 2

    return TouchstoneData(
        frequency=freqs,
        s_parameters=s_params,
        z0=z0,
        unit="Hz",
        parameter=param_type,
        format=data_format,
    )
