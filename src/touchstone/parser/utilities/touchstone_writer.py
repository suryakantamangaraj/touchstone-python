"""
Utilities for writing Touchstone data back to the .sNp file format.
"""

import io
from typing import Any, List, Optional

import numpy as np

from ..models.data_format import DataFormat
from ..models.frequency_unit import FrequencyUnit
from ..models.touchstone_data import TouchstoneData
from ..models.touchstone_options import TouchstoneOptions


def _format_value(value: Any) -> str:
    return f"{value:.10g}"


def _append_parameter(parts: List[str], s: complex, fmt: DataFormat):
    if fmt == DataFormat.RI:
        parts.append(_format_value(s.real))
        parts.append(_format_value(s.imag))
    elif fmt == DataFormat.MA:
        mag = np.abs(s)
        phase = np.angle(s, deg=True)
        parts.append(_format_value(mag))
        parts.append(_format_value(phase))
    elif fmt == DataFormat.DB:
        mag = np.abs(s)
        mag_db = 20 * np.log10(mag) if mag > 1e-20 else -400.0
        phase = np.angle(s, deg=True)
        parts.append(_format_value(mag_db))
        parts.append(_format_value(phase))


def write_snp(
    data: TouchstoneData, filepath: str, options: Optional[TouchstoneOptions] = None
) -> None:
    """
    Write Touchstone data to a file.

    Args:
        data (TouchstoneData): The data to write.
        filepath (str): The destination file path.
        options (Optional[TouchstoneOptions]): Export options. Defaults to data.options.
    """
    content = write_snp_to_string(data, options)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)


def write_snp_to_string(
    data: TouchstoneData, options: Optional[TouchstoneOptions] = None
) -> str:
    """
    Convert Touchstone data to its string representation.

    Args:
        data (TouchstoneData): The data to convert.
        options (Optional[TouchstoneOptions]): Export options. Defaults to data.options.

    Returns:
        str: The raw Touchstone file content as a string.
    """
    if options is None:
        options = data.options

    output = io.StringIO()

    for comment in data.comments:
        output.write(f"! {comment}\n")

    output.write(f"{options}\n")

    freq_divisors = {
        FrequencyUnit.HZ: 1.0,
        FrequencyUnit.KHZ: 1e3,
        FrequencyUnit.MHZ: 1e6,
        FrequencyUnit.GHZ: 1e9,
    }
    freq_div = freq_divisors.get(options.frequency_unit, 1.0)

    n = data.n_ports

    for p in range(data.n_freq):
        freq = data.frequency[p] / freq_div

        if n <= 2:
            parts = [_format_value(freq)]
            if n == 1:
                _append_parameter(
                    parts, data.s_parameters[p, 0, 0], options.data_format
                )
            else:
                _append_parameter(
                    parts, data.s_parameters[p, 0, 0], options.data_format
                )
                _append_parameter(
                    parts, data.s_parameters[p, 1, 0], options.data_format
                )
                _append_parameter(
                    parts, data.s_parameters[p, 0, 1], options.data_format
                )
                _append_parameter(
                    parts, data.s_parameters[p, 1, 1], options.data_format
                )
            output.write(" ".join(parts) + "\n")
        else:
            first_row = True
            for row in range(n):
                parts = []
                if first_row:
                    parts.append(_format_value(freq))
                    first_row = False

                for col in range(n):
                    _append_parameter(
                        parts, data.s_parameters[p, row, col], options.data_format
                    )

                output.write(" ".join(parts) + "\n")

    return output.getvalue()
