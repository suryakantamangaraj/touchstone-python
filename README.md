# touchstone.parser

**A high-performance, technically accurate Python library for Touchstone (.sNp) parsing and S-parameter analysis.**

[![PyPI version](https://img.shields.io/pypi/v/touchstone.parser.svg)](https://pypi.org/project/touchstone.parser/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![CI Status](https://github.com/suryakantamangaraj/touchstone-python/actions/workflows/ci.yml/badge.svg)](https://github.com/suryakantamangaraj/touchstone-python/actions)
[![Python Versions](https://img.shields.io/pypi/pyversions/touchstone.parser.svg)](https://pypi.org/project/touchstone.parser/)

`touchstone.parser` is a specialized library designed for RF/microwave engineers and researchers. It provides a robust, type-hinted, and NumPy-integrated API for reading and analyzing Touchstone files, ensuring high fidelity and compliance with the EIA/IBIS Touchstone® specification.

## Why touchstone.parser?

While other libraries exist, `touchstone.parser` is built with a focus on:
- **Performance**: Leveraging NumPy vectorization for parsing and processing large N-port data.
- **Developer Experience**: Modern Python features (dataclasses, type hints, PEP 517).
- **Correctness**: Strict adherence to the Touchstone standard, including handling the subtle port-ordering differences between 2-port and N-port files.

---

## Key Features

- **Standard Compliance**: Full support for Touchstone 1.1 and 2.0 file structures.
- **Multidimensional Analysis**: Handles N-port data (from `.s1p` up to `.sNp`) with efficient NumPy vectorization.
- **Metadata Aware**: Automatically parses frequency units (Hz, kHz, MHz, GHz), parameter types (S, Y, Z, G, H), and data formats (MA, DB, RI).
- **Reference Impedance**: Full support for custom reference impedance (`Z0`) specified in the option line.
- **Scientific Workflow**: Native NumPy array export for seamless integration with SciPy, Matplotlib, and scikit-rf.
- **Zero Dependencies**: Lightweight core with only `numpy` as a required dependency.

## Installation

Install the package via `pip`:

```bash
pip install touchstone.parser
```

For development or visualization support:

```bash
pip install "touchstone.parser[dev,viz]"
```

## Quickstart

### Basic Usage

```python
from touchstone.parser import read_snp

# Parse a 2-port Touchstone file (.s2p)
data = read_snp("measurements.s2p")

# Frequencies are automatically normalized to Hz
print(f"Frequency Range: {data.frequency.min():.2e} to {data.frequency.max():.2e} Hz")

# Access S-parameters as a complex NumPy array (shape: n_freq, n_ports, n_ports)
s_matrix = data.s_parameters

# Get S21 magnitude in dB
s21_db = data.magnitude(to_port=2, from_port=1, db=True)
```

### Advanced Analysis

```python
import matplotlib.pyplot as plt

# Plot S11 and S21 magnitude
plt.figure(figsize=(10, 6))
plt.plot(data.frequency / 1e9, data.magnitude(1, 1, db=True), label="S11 (Return Loss)")
plt.plot(data.frequency / 1e9, data.magnitude(2, 1, db=True), label="S21 (Insertion Loss)")
plt.xlabel("Frequency (GHz)")
plt.ylabel("Magnitude (dB)")
plt.title(f"S-Parameters (Z0 = {data.z0} Ω)")
plt.legend()
plt.grid(True, which='both', linestyle='--', alpha=0.5)
plt.show()
```

## Technical Specification

### Supported Formats
| Format | Description | Conversion |
|--------|-------------|------------|
| **RI** | Real / Imaginary | $S = R + jI$ |
| **MA** | Magnitude / Angle | $S = M \cdot e^{j\theta}$ (Angle in degrees) |
| **DB** | dB / Angle | $S = 10^{db/20} \cdot e^{j\theta}$ (Angle in degrees) |

### Port Ordering
The library correctly handles the special ordering for 2-port files defined by the standard:
- **2-Port**: `S11, S21, S12, S22`
- **N-Port (N > 2)**: `S11, S12, ..., S1N, S21, ..., SNN`

## Roadmap & Future Plans

We are actively working on expanding the library's capabilities. Planned features include:

- [ ] **Mixed-Mode S-Parameters**: Automatic conversion from single-ended to differential and common-mode parameters.
- [ ] **Network Operations**: Implementation of cascading (T-matrix) and de-embedding utilities.
- [ ] **Touchstone 2.0 Keywords**: Full support for `[Network Data]`, `[Noise Data]`, and `[Mixed-Mode Order]`.
- [ ] **Interactive Visualization**: Built-in support for interactive Smith charts and Bode plots using Plotly.
- [ ] **Export Utilities**: Ability to write/export `TouchstoneData` objects back to `.sNp` files.
- [ ] **Interpolation**: High-performance frequency re-sampling and spline interpolation.

## Development

We welcome contributions! To set up your local environment:

1. Clone the repository.
2. Create a virtual environment: `python -m venv venv`
3. Install dev dependencies: `pip install -e ".[dev]"`
4. Run tests: `pytest`
5. Run linting: `flake8 src tests` and `mypy src`

## License

Distributed under the MIT License. See `LICENSE` for more information.