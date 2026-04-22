# Contributing to touchstone.parser

Thank you for your interest in contributing to **touchstone.parser**! We welcome contributions from the community.

## Getting Started

1. **Fork** the repository on GitHub.
2. **Clone** your fork locally:
   ```bash
   git clone https://github.com/<your-username>/touchstone-python.git
   cd touchstone-python
   ```
3. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```
4. **Build and test** to ensure everything works:
   ```bash
   pip install .
   pytest
   ```

## Development Guidelines

### Code Style

- Follow the conventions defined in `.editorconfig`.
- Run `dotnet format` before submitting a PR to ensure consistent formatting.
- Use XML doc comments (`///`) on all public types and members.
- Follow standard Python naming conventions:
  - `PascalCase` for public members, types, and methods
  - `_camelCase` for private fields
  - `camelCase` for local variables and parameters

### Commit Messages

- Use clear, descriptive commit messages.
- Use the imperative mood: "Add feature" not "Added feature".
- Reference related issues where applicable: `Fix #42`.

### Testing

- Write pytest tests for all new features and bug fixes.
- Place tests in `tests/touchstone.parser.Tests/`.
- Use `FluentAssertions` for expressive assertions.
- Ensure all tests pass before submitting a PR.

### Pull Requests

1. Push your branch to your fork.
2. Open a Pull Request against the `main` branch.
3. Provide a clear description of the changes.
4. Ensure CI checks pass (build, lint, tests).
5. Respond to review feedback promptly.

## Reporting Issues

- Use [GitHub Issues](https://github.com/suryakantamangaraj/touchstone-python/issues) to report bugs or request features.
- Include steps to reproduce the issue, expected vs actual behavior, and relevant `.sNp` file samples where possible.

## Code of Conduct

Be respectful, inclusive, and constructive. We are committed to providing a welcoming and harassment-free experience for everyone.

## License

By contributing, you agree that your contributions will be licensed under the [MIT License](LICENSE).
