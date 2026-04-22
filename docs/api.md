# API Reference

The `touchstone.parser` package exports the following public API:

- `read_snp(filepath: str) -> TouchstoneData`
- `parse_string(content: str, n_ports: int = 0) -> TouchstoneData`
- `write_snp(data: TouchstoneData, filepath: str)`
- `write_snp_to_string(data: TouchstoneData) -> str`

## Data Models

- `TouchstoneData`: Represents parsed Touchstone data.
- `TouchstoneOptions`: Represents the parsed option line (`# HZ S MA R 50`).
- `FrequencyUnit`: Enum (`HZ`, `KHZ`, `MHZ`, `GHZ`)
- `ParameterType`: Enum (`S`, `Y`, `Z`, `G`, `H`)
- `DataFormat`: Enum (`RI`, `MA`, `DB`)

## Extensions

Located in `touchstone.parser.utilities`:
- `get_magnitude(data: TouchstoneData, to_port: int, from_port: int, db: bool = True) -> np.ndarray`
- `get_phase(data: TouchstoneData, to_port: int, from_port: int, deg: bool = True) -> np.ndarray`
- `normalize_frequency(freq: float, unit: str) -> float`
