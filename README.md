# touchstone.parser

**Python library for Touchstone `.sNp` parsing and S‑parameter analysis in RF/microwave engineering.**

[![PyPI version](https://img.shields.io/pypi/v/touchstone.parser.svg)](https://pypi.org/project/touchstone.parser/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Build Status](https://github.com/suryakantamangaraj/touchstone-python/workflows/CI/badge.svg)](https://github.com/suryakantamangaraj/touchstone-python/actions)

`touchstone.parser` is a minimalist, polished, and community-friendly library designed for reproducibility and automation in RF/microwave workflows. It provides a clean API to parse `.sNp` files into structured Python objects with full support for NumPy.

## Features

- **Robust Parsing**: Support for `.s1p`, `.s2p`, up to `.sNp` files.
- **Full Metadata Support**: Parses frequency units, parameter types (S, Y, Z, G, H), data formats (DB, MA, RI), and reference impedance.
- **Scientific Integration**: Direct conversion to NumPy arrays for easy analysis with SciPy and Matplotlib.
- **Modular Design**: Clean, type-hinted API designed for extensibility.

## Installation

```bash
pip install touchstone.parser
```

## Quickstart

```python
from touchstone.parser import read_snp

# Load a 2-port Touchstone file
data = read_snp("measurements.s2p")

# Access frequency data (in Hz)
print(data.frequency)

# Access S-parameters as a NumPy array (shape: n_freq x 2 x 2)
print(data.s_parameters)

# Access magnitude and phase at a specific frequency
s21_mag = data.magnitude("S", 2, 1)
s21_phase = data.phase("S", 2, 1)
```

## Contribution

Contributions are welcome! Please see our [Contributing Guidelines](CONTRIBUTING.md) for more details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.