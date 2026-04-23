"""
Utility functions for Touchstone data processing.

This sub-package provides conversion, analysis, and export utilities:

- **Frequency conversion** — :func:`~touchstone.parser.utilities.frequency_converter.normalize_frequency`,
  :func:`~touchstone.parser.utilities.frequency_converter.from_hz`,
  :func:`~touchstone.parser.utilities.frequency_converter.convert`
- **Network parameter math** — :func:`~touchstone.parser.utilities.network_parameter_extensions.db_to_mag`,
  :func:`~touchstone.parser.utilities.network_parameter_extensions.mag_to_db`,
  :func:`~touchstone.parser.utilities.network_parameter_extensions.ma_to_complex`,
  :func:`~touchstone.parser.utilities.network_parameter_extensions.db_to_complex`,
  :func:`~touchstone.parser.utilities.network_parameter_extensions.ri_to_complex`
- **Data extensions** — Insertion loss, return loss, VSWR, magnitude/phase extraction.
- **Writer** — :func:`~touchstone.parser.utilities.touchstone_writer.write_snp`,
  :func:`~touchstone.parser.utilities.touchstone_writer.write_snp_to_string`
"""

from .frequency_converter import convert, from_hz, get_multiplier, normalize_frequency
from .network_parameter_extensions import (
    db_to_complex,
    db_to_mag,
    deg_to_rad,
    ma_to_complex,
    mag_to_db,
    rad_to_deg,
    ri_to_complex,
    vswr_from_s11,
)
from .touchstone_data_extensions import (
    get_magnitude,
    get_phase,
    get_s11,
    get_s12,
    get_s21,
    get_s22,
    in_frequency_range,
    to_insertion_loss,
    to_return_loss,
    to_vswr,
)
from .touchstone_writer import write_snp, write_snp_to_string

__all__ = [
    "get_multiplier",
    "normalize_frequency",
    "from_hz",
    "convert",
    "db_to_mag",
    "mag_to_db",
    "deg_to_rad",
    "rad_to_deg",
    "ma_to_complex",
    "db_to_complex",
    "ri_to_complex",
    "vswr_from_s11",
    "get_magnitude",
    "get_phase",
    "to_insertion_loss",
    "to_return_loss",
    "to_vswr",
    "in_frequency_range",
    "get_s11",
    "get_s21",
    "get_s12",
    "get_s22",
    "write_snp",
    "write_snp_to_string",
]
