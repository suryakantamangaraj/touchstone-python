# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.1] - 2026-04-21

### Changed
- **Security Policy**: Updated `SECURITY.md` to reference the bug report template for submission structure, reducing redundancy.

## [1.0.0] - 2026-04-21

### Added
- **Visualization Example**: Added plotting demonstration using ScottPlot.
- **Project Governance**: Added Issue and Pull Request templates.
- **Centralized Package Management**: Migrated to `Directory.Packages.props`.
- **Strong-Name Signing**: Enabled assembly signing for enterprise compatibility.

### Fixed
- Resolved CI build failures related to FluentAssertions v8 API changes.
- Fixed whitespace and formatting issues in library and tests.

## [0.1.0] - 2026-04-20

### Added

- **Core parser** for Touchstone v1.0/v1.1 `.sNp` files (1-port through N-port).
- **Strongly typed models**: `NetworkParameter`, `FrequencyPoint`, `TouchstoneData`, `TouchstoneOptions`.
- Support for all three data formats: Real-Imaginary (RI), Magnitude-Angle (MA), Decibel-Angle (DB).
- Support for all frequency units: Hz, kHz, MHz, GHz.
- Support for all parameter types: S, Y, Z, H, G.
- **LINQ-friendly APIs**: `GetS11()`, `GetS21()`, `GetParameter(i, j)`, `GetFrequenciesIn()`.
- **RF calculations**: `ToInsertionLoss()`, `ToReturnLoss()`, `ToVswr()`.
- **Frequency filtering**: `InFrequencyRange()`, `Where()`.
- **Export utilities**: CSV export (`ToCsv()`, `ToCsvString()`) and Touchstone writer (`TouchstoneWriter`).
- **Frequency converter**: `FrequencyConverter.Convert()` between Hz, kHz, MHz, GHz.
- **NetworkParameter math**: `Conjugate()`, `Reciprocal()`, `Add()`, `Multiply()`.
- **Async parsing**: `ParseAsync()` with cancellation token support.
- **Multiple input sources**: Parse from file path, `Stream`, `TextReader`, or raw string.
- **Multi-target build**: `net6.0` and `netstandard2.1`.
- **CI/CD**: GitHub Actions workflows for build/test/lint and PyPI publishing.
- **Example application** demonstrating parsing, querying, and exporting Wi-Fi bandpass filter data.
- Comprehensive pytest test suite with FluentAssertions.
