# Releasing and Versioning Guide

This project follows [Semantic Versioning (SemVer)](https://semver.org/) and uses an automated CI/CD pipeline for releases.

## Versioning Strategy

The version number follows the `MAJOR.MINOR.PATCH` format:

- **MAJOR**: Incompatible API changes.
- **MINOR**: Add functionality in a backwards-compatible manner.
- **PATCH**: Backwards-compatible bug fixes.

The **Source of Truth** for the current version is the `version` field in the `pyproject.toml` file.

## Automated Release Process

The release process is fully automated via GitHub Actions using the [Publish to PyPI](.github/workflows/publish.yml) workflow.

### 1. Automatic Release (On Push to Main)
Whenever a push occurs on the `main` branch, the workflow evaluates the version in `pyproject.toml`:
- **Auto-Patch Increment**: If the version in `pyproject.toml` is already published (a Git tag exists), the workflow will automatically bump the patch version (e.g., `1.0.1` -> `1.0.2`), update `pyproject.toml`, push a silent commit to `main` with `[skip ci]`, tag the release, and publish.
- **Manual Version Bump**: If you manually edit `pyproject.toml` locally to a new, unpublished version (e.g., `1.1.0`) and push to `main`, the workflow detects that this version is new. It skips the auto-increment, tags `v1.1.0`, and publishes it directly.

### 2. Manual Release (Workflow Dispatch)
You can manually trigger a release or override the versioning from the GitHub UI, which is particularly useful for major or minor version changes:
1. Go to the **Actions** tab.
2. Select **Publish to PyPI**.
3. Click **Run workflow**.
4. Provide a **Manual version override** (e.g., `2.0.0`) to force a specific version. The workflow will update `pyproject.toml`, commit the change, tag the release, and publish.

### 3. Direct Tagging
If you manually create and push a Git tag starting with `v*` (e.g., `git tag v1.2.3 && git push origin v1.2.3`), the workflow will instantly build and publish that specific tag exactly as provided, without modifying the source code.

## Best Practices
1. **Rely on Auto-Patch**: For small bug fixes and minor updates, you don't need to manually update `pyproject.toml`. Simply merge to `main` and the system will automatically bump the patch version.
2. **Review Release Notes**: After an automated release, review the auto-generated notes on the GitHub Releases page to ensure they accurately reflect the changes.
3. **PyPI Authentication**: This repository uses PyPI Trusted Publishing (OIDC). Ensure Trusted Publishing is properly configured on PyPI to allow GitHub Actions to publish securely without API tokens.
