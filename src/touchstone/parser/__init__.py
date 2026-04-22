from .models.data_format import DataFormat
from .models.frequency_unit import FrequencyUnit
from .models.parameter_type import ParameterType
from .models.touchstone_data import TouchstoneData
from .models.touchstone_options import TouchstoneOptions
from .parsing.touchstone_parser import TouchstoneParser
from .parsing.touchstone_parser_exception import TouchstoneParserException
from .utilities.frequency_converter import normalize_frequency
from .utilities.network_parameter_extensions import (
    db_to_complex,
    db_to_mag,
    deg_to_rad,
    ma_to_complex,
    mag_to_db,
    rad_to_deg,
    ri_to_complex,
)
from .utilities.touchstone_writer import write_snp, write_snp_to_string

# Maintain backward compatible function aliases
read_snp = TouchstoneParser.parse
parse_string = TouchstoneParser.parse_string

__all__ = [
    "read_snp",
    "parse_string",
    "write_snp",
    "write_snp_to_string",
    "TouchstoneData",
    "TouchstoneOptions",
    "FrequencyUnit",
    "ParameterType",
    "DataFormat",
    "TouchstoneParser",
    "TouchstoneParserException",
    "normalize_frequency",
    "db_to_mag",
    "mag_to_db",
    "deg_to_rad",
    "rad_to_deg",
    "ma_to_complex",
    "db_to_complex",
    "ri_to_complex",
]
