# Touchstone Python vs .NET — Detailed Gap Analysis

> A comprehensive, file-by-file comparison identifying everything missing from `touchstone-python` relative to `touchstone-dotnet`.

---

## Executive Summary

The Python repo is a **functional port** of the .NET repo but is missing features across **5 major areas**: parser API surface, model richness, extension methods, test depth, and project infrastructure. There are **~40 discrete gaps** ranging from missing async parsing to absent GitHub templates.

---

## 1. Parser API Surface

### 1.1 Missing: `parse(stream)` Overload
- **.NET**: `TouchstoneParser.Parse(Stream stream, string? fileName)` — parse from any stream (network, memory, zip entry, etc.)
- **Python**: ❌ **Missing entirely**. Only `parse(filepath)` and `parse_string(content)` exist.
- **Impact**: Can't parse from in-memory streams, `BytesIO`, or network responses without first converting to string.

### 1.2 Missing: `parse(TextReader)` Overload
- **.NET**: `TouchstoneParser.Parse(TextReader reader, string? fileName)` — parse from any `TextReader`
- **Python**: ❌ **Missing entirely**. No equivalent that accepts file-like objects / `TextIO`.
- **Impact**: Can't pass open file handles, `StringIO`, or piped input.

### 1.3 Missing: `ParseAsync()` — Async Parsing
- **.NET**: `TouchstoneParser.ParseAsync(string filePath, CancellationToken ct)` with full async file I/O and cancellation support.
- **Python**: ❌ **Missing entirely**. No `async def parse_async()` or `asyncio` integration.
- **Impact**: Blocks the event loop in async applications (FastAPI, Jupyter async cells, etc.)
- **README claims it doesn't have it** — but .NET advertises it as a feature.

### 1.4 Missing: Public `DetectPortCount()` Method
- **.NET**: `TouchstoneParser.DetectPortCount(string fileName)` — a public static utility.
- **Python**: Port detection is **inline** inside `parse()` and **not exposed** as a public method.
- **Impact**: Users can't validate filenames programmatically without parsing.

### 1.5 Missing: Multiple Option Line Detection
- **.NET**: Parser explicitly **throws** `TouchstoneParserException("Multiple option lines found")` if a second `#` line appears.
- **Python**: Parser simply **breaks** on the first `#` line and ignores any subsequent ones. Silently swallows malformed files.
- **Impact**: Corrupted files pass validation silently.

### 1.6 Missing: Invalid Numeric Data Error Reporting
- **.NET DataLineTokenizer**: Throws `TouchstoneParserException("Invalid numeric value: '{token}'", lineNumber)` with the exact line number and bad token.
- **Python DataLineTokenizer**: Silently **`continue`s** past unparseable tokens with `except ValueError: continue`.
- **Impact**: Data corruption goes undetected; debugging is much harder.

---

## 2. Models — Missing Features

### 2.1 Missing: `FrequencyPoint` Class
- **.NET**: A dedicated `FrequencyPoint` class encapsulates a single frequency + its N×N `NetworkParameter[,]` matrix. Provides:
  - Indexer `fp[row, col]` → `NetworkParameter`
  - `GetParameterMatrix()` (returns a defensive copy)
  - `NumberOfPorts` property
  - `FrequencyHz` property
  - Input validation (negative frequency, non-square matrix, out-of-range index)
  - `ToString()` formatting
- **Python**: ❌ **No equivalent class**. Uses raw numpy 3D array `s_parameters[freq_idx, row, col]`.
- **Impact**: No per-point encapsulation, no per-point validation, harder to inspect individual frequency points.

### 2.2 Missing: `NetworkParameter` Struct/Class
- **.NET**: A dedicated `NetworkParameter` readonly struct with:
  - `Real`, `Imaginary` properties
  - Computed: `Magnitude`, `MagnitudeDb`, `PhaseDegrees`, `PhaseRadians`
  - Factory methods: `FromRealImaginary()`, `FromMagnitudeAngle()`, `FromDecibelAngle()`
  - Operations: `Conjugate()`, `Reciprocal()`
  - Static: `Zero`
  - Full `IEquatable<>`, `==`, `!=`, `GetHashCode()`, `ToString()`
- **Python**: ❌ **No equivalent class**. Uses raw `complex` values. Conversion utilities are standalone functions.
- **Impact**: No type safety for individual S-parameter values, no conjugate/reciprocal operations, no structured formatting.

### 2.3 Missing: `TouchstoneData.GetParameter(row, col)` Method
- **.NET**: Returns `IEnumerable<(double FrequencyHz, NetworkParameter Value)>` — a lazy enumerable of (freq, param) tuples across all frequency points.
- **Python**: Has `get_s(to_port, from_port)` but returns a raw numpy array, **not** tupled with frequency values.
- **Impact**: Users must manually zip with frequency array.

### 2.4 Missing: `TouchstoneData.Frequencies` Property
- **.NET**: `IEnumerable<double> Frequencies => FrequencyPoints.Select(fp => fp.FrequencyHz)`
- **Python**: Has `data.frequency` directly — **this exists** but is a numpy array (equivalent).

### 2.5 Missing: `TouchstoneData.Count` Property
- **.NET**: `int Count => FrequencyPoints.Count`
- **Python**: Has `n_freq` which is equivalent. ✅

### 2.6 Missing: `TouchstoneData[index]` Indexer
- **.NET**: `public FrequencyPoint this[int index] => FrequencyPoints[index]` — access any frequency point by index.
- **Python**: ❌ **No `__getitem__` indexer**. Must access `data.s_parameters[index]` directly.
- **Impact**: Less ergonomic point-by-point access.

### 2.7 Missing: `TouchstoneOptions.Default` Static Property
- **.NET**: `TouchstoneOptions.Default` — a cached default instance.
- **Python**: ❌ No static default. Must construct `TouchstoneOptions()` each time.

### 2.8 Missing: Null/Argument Validation in Models
- **.NET**: `TouchstoneData` constructor validates: `null` options, `null` frequencyPoints, `null` comments, `numberOfPorts < 1`.
- **Python**: Only validates shape mismatch between frequency and s_parameters. ❌ No validation for negative ports, null options, etc.

---

## 3. Utilities & Extensions — Missing Features

### 3.1 Missing: `GetS11()`, `GetS21()`, `GetS12()`, `GetS22()` Shortcut Methods
- **.NET**: Four named extension methods for the common 2-port parameters, each returning `IEnumerable<(double FrequencyHz, NetworkParameter Value)>`.
- **Python**: ❌ **None of these exist**. Users must call `data.get_s(1,1)`, `data.get_s(2,1)`, etc.
- **Impact**: Less discoverable API, more verbose user code.

### 3.2 Missing: `GetFrequenciesIn(FrequencyUnit unit)` Method
- **.NET**: Returns frequencies converted to any unit (GHz, MHz, etc.)
- **Python**: ❌ **Missing**. Users must manually divide `data.frequency / 1e9`.
- **Impact**: No built-in unit conversion for output.

### 3.3 Missing: `MinFrequencyHz()` / `MaxFrequencyHz()` Methods
- **.NET**: Convenience extension methods returning min/max frequency.
- **Python**: ❌ **Missing** as named methods. Users must use `data.frequency.min()`.

### 3.4 Missing: `Where(predicate)` — Generic Filtering
- **.NET**: `TouchstoneData.Where(Func<FrequencyPoint, bool> predicate)` — filter with any predicate.
- **Python**: ❌ **Missing**. Only `in_frequency_range(min, max)` exists.
- **Impact**: Can't filter by parameter magnitude threshold, VSWR limit, etc.

### 3.5 Missing: `FrequencyConverter.Convert(value, from, to)` — Unit-to-Unit Conversion
- **.NET**: Full bidirectional frequency converter: `ToHz()`, `FromHz()`, `Convert()`, `GetMultiplier()`.
- **Python**: Only has `normalize_frequency(freq, unit)` → Hz. ❌ No `from_hz()`, no unit-to-unit conversion, no `get_multiplier()`.
- **Impact**: Can't convert Hz back to GHz/MHz for display or export.

### 3.6 Missing: `NetworkParameterExtensions` — Complex Arithmetic
- **.NET**: Extension methods for `NetworkParameter`:
  - `Add()`, `Subtract()`, `Multiply()` — complex arithmetic
  - `ApproximatelyEquals(other, tolerance)` — tolerance comparison
  - `ToDecibels()`, `ToMagnitude()`, `ToPhaseRadians()`, `ToPhaseDegrees()` — convenience wrappers
- **Python**: ❌ **No equivalent** for complex arithmetic extensions or approximate equality.
- **Impact**: Users must do manual complex math.

### 3.7 Missing: CSV Export with Configurable Format/Unit
- **.NET `ToCsv()`**: Accepts `FrequencyUnit` and `DataFormat` parameters. Headers change dynamically (e.g., `S11_dB`, `S11_Re`, `S11_Mag`).
- **Python `to_csv()`**: Always exports as `S11_Mag` / `S11_Phase(deg)`. ❌ No format or unit configuration.
- **Impact**: Users can't export in dB/angle or RI format via CSV.

### 3.8 Missing: `TouchstoneWriter.Write(data, filePath)` Direct File Write
- **.NET**: `TouchstoneWriter.Write(data, filePath, options?)` — writes directly to file.
- **Python**: Has `write_snp(data, filepath)` — ✅ **This exists and is equivalent**.

---

## 4. Testing — Missing Coverage

### 4.1 Missing Edge Case Tests (14 tests → 1 test)

| .NET Edge Case Test | Python Equivalent |
|---|---|
| `Parse_EmptyString_WithKnownPortCount_ReturnsEmptyData` | ❌ Missing |
| `Parse_EmptyString_WithoutFileName_ThrowsException` | ❌ Missing |
| `Parse_OnlyComments_WithKnownPortCount_ReturnsEmptyData` | ❌ Missing |
| `Parse_OnlyComments_WithoutFileName_ThrowsException` | ❌ Missing |
| `Parse_DuplicateOptionLine_ThrowsException` | ❌ Missing (Python doesn't detect this) |
| `Parse_InvalidNumericData_ThrowsException` | ❌ Missing (Python silently skips) |
| `FrequencyPoint_NegativeFrequency_Throws` | ❌ Missing (no FrequencyPoint class) |
| `FrequencyPoint_NonSquareMatrix_Throws` | ❌ Missing |
| `FrequencyPoint_IndexOutOfRange_Throws` | ❌ Missing |
| `TouchstoneData_ZeroPorts_Throws` | ❌ Missing |
| `TouchstoneData_NullOptions_Throws` | ❌ Missing |
| `Parse_InlineCommentInData_HandledCorrectly` | ❌ Missing |
| `Parse_MixedCaseOptions_ParsesCorrectly` | ❌ Missing |
| `Parse_ExtraWhitespace_ParsesCorrectly` | ❌ Missing |
| `Parse_NullPath_ThrowsArgumentNullException` | ❌ Missing |
| `OptionLineParser_NullLine_ThrowsArgumentNullException` | ❌ Missing |
| `DetectPortCount_NullFileName_ThrowsArgumentNullException` | ❌ Missing |
| **Only** `test_missing_file_throws` | ✅ Present |

### 4.2 Missing Parser Tests (12 tests → 3 tests)

| .NET Parser Test | Python Equivalent |
|---|---|
| `Parse_Simple1Port_ParsesCorrectly` (full) | ✅ Partial (only checks n_ports, n_freq, freq[0]) |
| `Parse_Simple1Port_FrequenciesAreInHz` | ❌ Missing |
| `Parse_Simple1Port_ParameterValuesAreCorrect` | ❌ Missing |
| `Parse_Simple1Port_CommentsExtracted` | ❌ Missing |
| `Parse_BandpassFilter_ParsesCorrectly` | ❌ Missing |
| `Parse_BandpassFilter_2PortOrdering` | ❌ Missing |
| `Parse_Amplifier_RiFormat` | ❌ Missing |
| `Parse_Coupler3Port_ParsesCorrectly` | ❌ Missing |
| `Parse_Coupler3Port_MatrixValues` | ❌ Missing |
| `Parse_CommentsFile_ExtractsAllComments` | ✅ Partial |
| `Parse_MinimalFile_ParsesCorrectly` | ✅ Partial |
| `ParseString_ParsesCorrectly` | ❌ Missing |
| `Parse_Stream_ParsesCorrectly` | ❌ Missing (no stream parsing) |
| `ParseAsync_ParsesCorrectly` | ❌ Missing (no async parsing) |
| `Parse_NonExistentFile_ThrowsFileNotFoundException` | ✅ In edge cases |
| `DetectPortCount` (Theory, 7 cases) | ❌ Missing |
| `GetParameter_ReturnsCorrectEnumerable` | ❌ Missing |
| `Frequencies_ReturnsAllFrequencies` | ❌ Missing |

### 4.3 Missing OptionLineParser Tests (11 tests → 1 test)

| .NET Test | Python |
|---|---|
| `Parse_FullOptionLine_ReturnsCorrectOptions` | ✅ Equivalent |
| `Parse_MhzRiFormat_ReturnsCorrectOptions` | ❌ Missing |
| `Parse_KhzMaFormat_ReturnsCorrectOptions` | ❌ Missing |
| `Parse_HzZParameters_ReturnsCorrectOptions` | ❌ Missing |
| `Parse_LowerCase_ParsesCorrectly` | ❌ Missing |
| `Parse_WithInlineComment_IgnoresComment` | ❌ Missing |
| `Parse_MinimalOptionLine_UsesDefaults` | ❌ Missing |
| `Parse_HybridParameters_ReturnsCorrectType` | ❌ Missing |
| `Parse_InverseHybridParameters_ReturnsCorrectType` | ❌ Missing |
| `Parse_InvalidImpedance_ThrowsException` | ❌ Missing |
| `Parse_MissingImpedanceValue_ThrowsException` | ❌ Missing |
| `Parse_ToString_ProducesValidOptionLine` | ❌ Missing |

### 4.4 Missing NetworkParameter Tests (14 tests → 1 test)

| .NET Test | Python |
|---|---|
| `FromRealImaginary_StoresCorrectly` | ❌ Missing (no class) |
| `FromMagnitudeAngle_0Degrees` | ❌ Missing |
| `FromMagnitudeAngle_90Degrees` | ❌ Missing |
| `FromDecibelAngle_0dB` | ❌ Missing |
| `FromDecibelAngle_Minus20dB` | ❌ Missing |
| `Magnitude_3_4_Returns5` | ❌ Missing |
| `MagnitudeDb_Unit_Returns0` | ❌ Missing |
| `MagnitudeDb_Zero_ReturnsNegInfinity` | ❌ Missing |
| `PhaseDegrees_90` | ❌ Missing |
| `RoundTrip_RI_MA_RI` (Theory, 3 cases) | ❌ Missing |
| `RoundTrip_RI_DB_RI` (Theory, 2 cases) | ❌ Missing |
| `Conjugate_NegatesImaginary` | ❌ Missing |
| `Reciprocal_Correct` | ❌ Missing |
| `Reciprocal_Zero_Throws` | ❌ Missing |
| `Add_ReturnsSum` | ❌ Missing |
| `Multiply_ReturnsProduct` | ❌ Missing |
| `Equality_Same` | ❌ Missing |
| `ApproximatelyEquals_Close` | ❌ Missing |
| **Only** basic conversion tests | ✅ Present |

### 4.5 Missing Writer Tests

| .NET Test | Python |
|---|---|
| `RoundTrip_1Port_RI` | ❌ Missing (Python has roundtrip but only for 2-port) |
| `RoundTrip_2Port_DB` | ❌ Missing |
| `Write_WithDifferentOptions_ConvertsFormat` | ❌ Missing |
| `Write_PreservesComments` | ✅ Partial |
| `RoundTrip_3Port` | ❌ Missing |

### 4.6 Missing Data Extensions Tests

| .NET Test | Python |
|---|---|
| `GetS11_ReturnsCorrectCount` | ❌ Missing (no GetS11 method) |
| `GetS21_ReturnsCorrectValues` | ❌ Missing |
| `GetFrequenciesIn_ConvertsCorrectly` | ❌ Missing |
| `MinMaxFrequency_Correct` | ❌ Missing |
| `ToCsvString_ProducesValidCsv` | ❌ Missing (Python CSV test doesn't verify format options) |
| `ToCsvString_RiFormat_ProducesCorrectHeaders` | ❌ Missing |
| `GetParameter_InvalidIndices_ThrowsArgumentOutOfRangeException` | ❌ Missing |

### 4.7 Missing N-Port Tests

| .NET Test | Python |
|---|---|
| `Parse_4Port_ParsesCorrectly` (detailed) | ✅ Basic check exists |
| `Parse_4Port_SecondPoint` (value checks) | ❌ Missing |

### 4.8 Missing Stress Tests
- **.NET**: Tests **parsing** 10,000 frequency points from a **generated string** via `TouchstoneParser.ParseString()`.
- **Python**: Only tests **constructing** a `TouchstoneData` object with random data. ❌ **Does not test the actual parser** under load.

---

## 5. Project Infrastructure — Missing Items

### 5.1 Missing: `.github/ISSUE_TEMPLATE/` Directory
- **.NET**: Has `bug_report.md` and `feature_request.md` issue templates.
- **Python**: ❌ **No issue templates at all**.

### 5.2 Missing: `.github/PULL_REQUEST_TEMPLATE.md`
- **.NET**: Has a detailed PR template with type-of-change checkboxes, test checklist, etc.
- **Python**: ❌ **No PR template**.

### 5.3 Missing: `.github/dependabot.yml`
- **.NET**: Configured for weekly NuGet + GitHub Actions dependency updates.
- **Python**: ❌ **No Dependabot** for pip/PyPI or GitHub Actions.

### 5.4 Missing: `.editorconfig`
- **.NET**: Comprehensive `.editorconfig` with C#-specific formatting, naming conventions, and code quality rules.
- **Python**: ❌ **No `.editorconfig`**. Has `black` and `isort` config in `pyproject.toml` but no cross-editor config.

### 5.5 Missing: `icon.png` — Package Icon
- **.NET**: Has a 341KB `icon.png` used as the NuGet package icon.
- **Python**: ❌ **No package icon** for PyPI.

### 5.6 Missing: Plotting Example
- **.NET**: Has `Touchstone.Plotting.Example` using ScottPlot to generate S-parameter plots with saved PNG output.
- **Python**: The `quickstart.py` example has a matplotlib section, but it **calls `data.magnitude()` and `data.phase()` which don't exist** as methods on `TouchstoneData`. The example is **broken**.

### 5.7 Missing: Comprehensive Parser Example
- **.NET**: `Touchstone.Parser.Examples/Program.cs` is a **102-line** demo covering parsing, LINQ queries, passband analysis, VSWR table, CSV export, and Touchstone re-export with beautiful ASCII formatting.
- **Python**: `quickstart.py` is **58 lines** and uses APIs that **don't match the actual codebase** (`data.magnitude()`, `data.phase()`). It's incomplete and broken.

### 5.8 Missing: Benchmarks
- **.NET**: Has a full `Touchstone.Parser.Benchmarks` project using BenchmarkDotNet with `[MemoryDiagnoser]` for memory allocation tracking.
- **Python**: `.benchmarks` directory is **empty**. `pytest-benchmark` is listed as a dev dependency but **no benchmark tests exist**.

### 5.9 Missing: Dual Package Registry Publishing
- **.NET `publish.yml`**: Publishes to **both** NuGet.org **and** GitHub Packages.
- **Python `publish.yml`**: Only publishes to PyPI. ❌ **No GitHub Packages**.

### 5.10 Missing: NuGet Artifact Upload in CI
- **.NET `ci.yml`**: Runs `dotnet pack` as validation and uploads the `.nupkg` as a CI artifact with 7-day retention.
- **Python `ci.yml`**: ❌ **No package build validation** in CI. Doesn't build a wheel/sdist to verify packaging works.

### 5.11 Missing: NuGet Cache
- **.NET `ci.yml`**: Uses `actions/cache@v4` for NuGet package caching.
- **Python `ci.yml`**: ❌ **No pip cache** configured. Slower CI runs.

### 5.12 Outdated GitHub Action Versions
- **.NET CI**: Uses `actions/checkout@v4`, `actions/setup-dotnet@v5`, `actions/cache@v4`, `codecov/codecov-action@v6`
- **Python CI**: Uses `actions/checkout@v3`, `actions/setup-python@v4` — ❌ **outdated by 1-2 major versions**.
- **Python CD**: Also uses `actions/checkout@v3`, `actions/setup-python@v4` — ❌ **outdated**.

### 5.13 Missing: Redundant CD Workflow
- **Python** has **both** `cd.yml` (triggered on release, uses `twine`) **and** `publish.yml` (triggered on push/tag, uses `gh-action-pypi-publish`). These **overlap** and could publish the same version twice or conflict.
- **.NET**: Has a single `publish.yml` — clean and non-redundant.

---

## 6. Documentation Gaps

### 6.1 Missing: Auto-generated API Docs
- **.NET `docs/`**: Uses **DocFX** with `docfx.json` to auto-generate API reference from XML doc comments. Has `_site/` build output.
- **Python `docs/`**: Uses **MkDocs** with `mkdocs.yml`, but the `docs/api/` directory is **empty** — no auto-generated docs from docstrings. The `api.md` is a **manually written** stub.

### 6.2 README Inaccuracies
- **Python README** claims "LINQ-friendly APIs" and mentions `GetS11()`, `GetS21()`, `GetParameter(i, j)` — ❌ **None of these methods exist** in the Python codebase.
- **Python README** claims "Zero dependencies — pure Python, no external packages" — ❌ **False**: the library requires `numpy>=1.20.0`.
- **Python README** shows `FrequencyPoint` and `NetworkParameter` as class names — ❌ **These classes don't exist** in the Python code.

### 6.3 Missing: Ecosystem Cross-reference
- **.NET README**: Links to the Python version: "check out the Python version for Python-based workflows"
- **Python README**: ❌ **Does not link back** to the .NET version.

---

## 7. Code Quality Differences

| Aspect | .NET | Python |
|---|---|---|
| XML Doc Comments | ✅ Every public member documented | ❌ Inconsistent — some methods lack docstrings |
| Null/Input Validation | ✅ Comprehensive `ArgumentNullException`, `ArgumentOutOfRangeException` | ❌ Minimal — mostly relies on Python duck typing |
| Exception line numbers | ✅ `TouchstoneParserException` carries `LineNumber` | ❌ No line number tracking in exceptions |
| Immutability | ✅ `sealed` classes, `readonly struct`, `IReadOnlyList<>` | ✅ `frozen=True` dataclasses (good) |
| Defensive copies | ✅ `FrequencyPoint.GetParameterMatrix()` returns cloned arrays | ❌ Not applicable (numpy arrays are mutable) |
| Code analyzers | ✅ `Microsoft.CodeAnalysis.NetAnalyzers`, `TreatWarningsAsErrors` | ✅ Has `flake8`, `mypy`, `black`, `isort` |
| SourceLink | ✅ Configured for debugging into source | ❌ Not applicable for Python |

---

## Summary: Missing Item Count

| Category | Missing Items |
|---|---|
| Parser API methods | 6 |
| Model classes/features | 8 |
| Extension/utility methods | 8 |
| Test cases (approx) | ~65 individual tests |
| Infrastructure files | 13 |
| Documentation issues | 3 |
| **Total** | **~40 discrete gaps** |

---

> [!IMPORTANT]
> The most critical gaps are: (1) missing `FrequencyPoint` and `NetworkParameter` classes that form the foundation of the type-safe API, (2) broken/inaccurate examples and README claims, (3) silent error swallowing in the tokenizer, and (4) ~65 missing test cases.
