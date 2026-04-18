# Contributing to touchstone.parser

First off, thank you for considering contributing to `touchstone.parser`! It's people like you that make the open-source RF/microwave community great.

## How Can I Contribute?

### Reporting Bugs
- Check the [Issues](https://github.com/suryakantamangaraj/touchstone-python/issues) to see if the bug has already been reported.
- Use a clear and descriptive title.
- Describe the exact steps to reproduce the problem.
- Include the `.sNp` file (or a snippet) that caused the issue.

### Suggesting Enhancements
- Open an issue to discuss your idea before implementing it.
- Explain why this enhancement would be useful to other users.

### Pull Requests
1. Fork the repo and create your branch from `dev`.
2. Install development dependencies: `pip install -e ".[dev]"`.
3. Ensure the test suite passes: `pytest`.
4. Follow PEP 8 and use Type Hints.
5. Run linting: `black .`, `isort .`, `flake8`.

## Development Setup

```bash
git clone https://github.com/suryakantamangaraj/touchstone-python.git
cd touchstone-python
python -m venv venv
source venv/bin/activate
pip install -e ".[dev]"
```

## Community

By contributing, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md).
