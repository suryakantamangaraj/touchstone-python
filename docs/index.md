# touchstone.parser Documentation

Welcome to the **touchstone.parser** API documentation.

This library provides a clean, modular, and enterprise-ready way to parse Touchstone (`.sNp`) files in Python.

## Getting Started

Install the package:

```bash
pip install touchstone.parser
```

Then parse your first file:

```python
from touchstone.parser import TouchstoneParser

data = TouchstoneParser.parse("filter.s2p")

# Query S21 insertion loss
il = data.to_insertion_loss()
for f, val in zip(data.frequency, il):
    freq_ghz = f / 1e9
    print(f"{freq_ghz:.3f} GHz -> IL = {val:.2f} dB")
```

For more details, see the [README on GitHub](https://github.com/suryakantamangaraj/touchstone-python).

## Key Features

- **Parse `.sNp` files** into strongly typed Python objects.
- **Multi-port support** (1-port through N-port).
- **All data formats** (RI, MA, DB).
- **All frequency units** (Hz, kHz, MHz, GHz).
- **Numpy integration** for fast vector operations.
- **RF calculations** (Magnitude, Phase, Conversions).

## Explore the API

Browse the full [API Reference](api.md) to see all available types, methods, and extensions.
