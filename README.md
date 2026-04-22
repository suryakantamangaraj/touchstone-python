# touchstone.parser

> **A Python library for Touchstone `.sNp` parsing and S‑parameter analysis in RF/microwave engineering.**

[![PyPI](https://img.shields.io/pypi/v/touchstone.parser?style=flat-square&logo=pypi&label=PyPI)](https://pypi.org/project/touchstone.parser/)
[![PyPI Downloads](https://img.shields.io/pypi/dm/touchstone.parser?style=flat-square&logo=pypi)](https://pypi.org/project/touchstone.parser/)
[![Build](https://img.shields.io/github/actions/workflow/status/suryakantamangaraj/touchstone-python/ci.yml?branch=main&style=flat-square&logo=github&label=CI)](https://github.com/suryakantamangaraj/touchstone-python/actions/workflows/ci.yml)
[![Coverage](https://img.shields.io/codecov/c/github/suryakantamangaraj/touchstone-python?style=flat-square&logo=codecov)](https://codecov.io/gh/suryakantamangaraj/touchstone-python)
[![Docs](https://img.shields.io/badge/docs-GitHub%20Pages-blue?style=flat-square&logo=github)](https://suryakantamangaraj.github.io/touchstone-python/)
[![License](https://img.shields.io/github/license/suryakantamangaraj/touchstone-python?style=flat-square)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org/)

**touchstone.parser** is a clean, modular, enterprise-ready Python library for parsing [Touchstone](https://ibis.org/) (`.sNp`) files — the industry-standard format for RF and microwave S‑parameter data. It provides strongly typed classes, LINQ-friendly APIs, and seamless integration into simulation and analysis workflows.

---

## ✨ Features

- **Parse `.sNp` files** into strongly typed Python classes (`TouchstoneData`, `FrequencyPoint`, `NetworkParameter`)
- **Multi-port support** — 1‑port through N‑port networks
- **All data formats** — Real/Imaginary (RI), Magnitude/Angle (MA), Decibel/Angle (DB)
- **All frequency units** — Hz, kHz, MHz, GHz with automatic normalization
- **All parameter types** — S, Y, Z, H, G
- **LINQ-friendly APIs** — query S‑parameters with `GetS11()`, `GetS21()`, `GetParameter(i, j)`
- **RF calculations** — insertion loss, return loss, VSWR out of the box
- **Export utilities** — CSV export and Touchstone writer for round-trip fidelity
- **Zero dependencies** — pure Python, no external packages


---

## 📦 Installation

```bash
pip install touchstone.parser
```

Or via the PyPI Package Manager:

```
pip install touchstone.parser
```

---

## 🚀 Quick Start

```python
from touchstone.parser import TouchstoneParser

# Parse a Touchstone file
data = TouchstoneParser.parse("filter.s2p")

print(f"Ports: {data.n_ports}")
print(f"Frequency points: {data.n_freq}")

# Query S21 insertion loss
il = data.to_insertion_loss()
for f, val in zip(data.frequency, il):
    freq_ghz = f / 1e9
    print(f"{freq_ghz:.3f} GHz → IL = {val:.2f} dB")

# Filter to a frequency range
passband = data.in_frequency_range(2.0e9, 3.0e9)

# Compute VSWR
vswr = data.to_vswr()
for f, val in zip(data.frequency, vswr):
    print(f"VSWR = {val:.3f}")

# Export to CSV
data.to_csv("output.csv")
```

---

## 📖 API Overview

### Parsing

| Method | Description |
|--------|-------------|
| `TouchstoneParser.parse(filepath)` | Parse from a file path |
| `TouchstoneParser.parse_string(content, n_ports?)` | Parse from a raw string |

### Data Access

| Method | Description |
|--------|-------------|
| `data.get_s(to_port, from_port)` | Get S‑parameters across all frequencies |
| `data.frequency` | All frequency values in Hz |
| `data.s_parameters` | 3D numpy array of all parameters |

### RF Calculations

| Method | Description |
|--------|-------------|
| `data.to_insertion_loss()` | \|S21\| insertion loss in dB |
| `data.to_return_loss()` | \|S11\| return loss in dB |
| `data.to_vswr()` | VSWR from S11 |

### Filtering & Export

| Method | Description |
|--------|-------------|
| `data.in_frequency_range(min_hz, max_hz)` | Filter to frequency range |
| `data.to_csv(writer)` | Export to CSV file or path |
| `data.to_csv_string()` | Export to CSV string |
| `write_snp(data, filepath)` | Write back to Touchstone format |

### Utilities

| Method | Description |
|--------|-------------|
| `normalize_frequency(val, unit)` | Convert to Hz |
| `db_to_mag(db)` | Convert DB to magnitude |
| `mag_to_db(mag)` | Convert magnitude to DB |
| `ma_to_complex(mag, deg)` | Create from MA |
| `db_to_complex(dB, deg)` | Create from DB |

---

## 🏗️ Project Structure

```
touchstone-python/
├── src/
│   └── touchstone/parser/          # Core library
│       ├── models/                  # Domain models (enums, data classes)
│       ├── parsing/                 # Parser engine
│       └── utilities/               # Converters, extensions, writer
├── tests/                           # pytest test suite
├── pyproject.toml                   # Project metadata and dependencies
├── mkdocs.yml                       # Documentation configuration
└── .github/workflows/               # GitHub Actions CI/CD
```

---

## 🔧 Supported Formats

| Feature | Supported |
|---------|-----------|
| Touchstone v1.0 / v1.1 | ✅ |
| 1‑port (`.s1p`) | ✅ |
| 2‑port (`.s2p`) | ✅ |
| Multi-port (`.s3p`, `.s4p`, ...) | ✅ |
| Real-Imaginary (RI) | ✅ |
| Magnitude-Angle (MA) | ✅ |
| Decibel-Angle (DB) | ✅ |
| Hz / kHz / MHz / GHz | ✅ |
| S / Y / Z / H / G parameters | ✅ |
| Comments and metadata | ✅ |
| Touchstone v2.0 keywords | 🔜 Planned |

---

## 🧪 Running Tests

```bash
pytest --verbosity normal
```

---

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## 💬 Community

- ⭐ **Star this repo** and related RF/microwave projects to help them grow - then mention your project in context to build visibility.
- 💡 **Share feedback** via [GitHub Discussions](https://github.com/suryakantamangaraj/touchstone-python/discussions) - we'd love to hear how you're using the library, what's working, and what could be better.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 💖 Support & Funding

If this library helps you in your RF/microwave engineering work, consider supporting its maintenance and the development of new features:
- **[Sponsor on GitHub](https://github.com/sponsors/suryakantamangaraj)**
- ⭐ **Star the project** to help it gain visibility in the engineering community.

---

## 📚 Resources

- [Touchstone File Format Specification (IBIS)](https://ibis.org/)
- [S-parameter — Wikipedia](https://en.wikipedia.org/wiki/Scattering_parameters)
- [PyPI Package](https://www.pypi.org/packages/touchstone.parser)

---

<p align="center">
  Made by <a href="https://suryaraj.com">suryamangaraj</a> · Built for the RF/microwave engineering community 📡
</p>
