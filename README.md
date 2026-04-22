# touchstone.parser

> **A Python library for Touchstone `.sNp` parsing and S‑parameter analysis in RF/microwave engineering.**

[![PyPI](https://img.shields.io/pypi/v/touchstone.parser?style=flat-square&logo=nuget&label=PyPI)](https://www.pypi.org/packages/touchstone.parser)
[![PyPI Downloads](https://img.shields.io/pypi/dm/touchstone.parser?style=flat-square&logo=nuget)](https://www.pypi.org/packages/touchstone.parser)
[![Build](https://img.shields.io/github/actions/workflow/status/suryakantamangaraj/touchstone-python/ci.yml?branch=main&style=flat-square&logo=github&label=CI)](https://github.com/suryakantamangaraj/touchstone-python/actions/workflows/ci.yml)
[![Coverage](https://img.shields.io/codecov/c/github/suryakantamangaraj/touchstone-python?style=flat-square&logo=codecov)](https://codecov.io/gh/suryakantamangaraj/touchstone-python)
[![Docs](https://img.shields.io/badge/docs-GitHub%20Pages-blue?style=flat-square&logo=github)](https://suryakantamangaraj.github.io/touchstone-python/)
[![License](https://img.shields.io/github/license/suryakantamangaraj/touchstone-python?style=flat-square)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8%2B-512BD4?style=flat-square&logo=dotnet)](https://python.org/)

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
- **Async support** — `ParseAsync()` with cancellation token
- **Cross-platform** — targets `net6.0` and `netstandard2.1`
- **Ecosystem breadth** — check out the [Python version](https://github.com/suryakantamangaraj/touchstone-python) for Python-based workflows
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

```csharp
using touchstone.parser.Parsing;
using touchstone.parser.Utilities;
using touchstone.parser.Models;

// Parse a Touchstone file
var data = TouchstoneParser.Parse("filter.s2p");

Console.WriteLine($"Ports: {data.NumberOfPorts}");
Console.WriteLine($"Frequency points: {data.Count}");

// Query S21 insertion loss with LINQ
foreach (var (freqHz, param) in data.GetS21())
{
    double freqGhz = FrequencyConverter.FromHz(freqHz, FrequencyUnit.GHz);
    Console.WriteLine($"{freqGhz:F3} GHz → S21 = {param.MagnitudeDb:F2} dB");
}

// Filter to a frequency range
var passband = data.InFrequencyRange(2.0e9, 3.0e9);

// Compute VSWR
foreach (var (freqHz, vswr) in data.ToVswr())
{
    Console.WriteLine($"VSWR = {vswr:F3}");
}

// Export to CSV
using var writer = new StreamWriter("output.csv");
data.ToCsv(writer, FrequencyUnit.GHz, DataFormat.DecibelAngle);
```

---

## 📖 API Overview

### Parsing

| Method | Description |
|--------|-------------|
| `TouchstoneParser.Parse(filePath)` | Parse from a file path |
| `TouchstoneParser.Parse(stream, fileName?)` | Parse from a stream |
| `TouchstoneParser.Parse(textReader, fileName?)` | Parse from a TextReader |
| `TouchstoneParser.ParseString(content, fileName?)` | Parse from a raw string |
| `TouchstoneParser.ParseAsync(filePath, ct)` | Async file parsing |

### Data Access (LINQ-friendly)

| Method | Description |
|--------|-------------|
| `data.GetParameter(row, col)` | Get any S‑parameter across all frequencies |
| `data.GetS11()` / `GetS21()` / `GetS12()` / `GetS22()` | Common 2‑port shortcuts |
| `data.Frequencies` | All frequency values in Hz |
| `data.GetFrequenciesIn(FrequencyUnit.GHz)` | Frequencies in any unit |
| `data[index]` | Access a specific frequency point |

### RF Calculations

| Method | Description |
|--------|-------------|
| `data.ToInsertionLoss()` | \|S21\| insertion loss in dB |
| `data.ToReturnLoss()` | \|S11\| return loss in dB |
| `data.ToVswr()` | VSWR from S11 |

### Filtering & Export

| Method | Description |
|--------|-------------|
| `data.InFrequencyRange(minHz, maxHz)` | Filter to frequency range |
| `data.Where(predicate)` | Custom filtering |
| `data.ToCsv(writer, unit, format)` | Export to CSV |
| `data.ToCsvString(unit, format)` | Export to CSV string |
| `TouchstoneWriter.Write(data, filePath)` | Write back to Touchstone format |

### Utilities

| Method | Description |
|--------|-------------|
| `FrequencyConverter.Convert(val, from, to)` | Convert between frequency units |
| `NetworkParameter.FromRealImaginary(re, im)` | Create from RI |
| `NetworkParameter.FromMagnitudeAngle(mag, deg)` | Create from MA |
| `NetworkParameter.FromDecibelAngle(dB, deg)` | Create from DB |

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
