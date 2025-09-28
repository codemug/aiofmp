# Release Process Documentation

This document describes the automated release process for aiofmp using python-semantic-release and GitHub Actions.

## Overview

The release process is fully automated and triggered by commits to the `main` branch. It uses:

- **python-semantic-release**: For automated versioning based on conventional commits
- **GitHub Actions**: For CI/CD pipeline
- **PyPI**: For package distribution
- **Conventional Commits**: For commit message standardization

## Workflow

### 1. Commit Message Analysis

python-semantic-release analyzes commit messages to determine the next version:

- `feat:` → Minor version bump (1.0.0 → 1.1.0)
- `fix:` → Patch version bump (1.0.0 → 1.0.1)
- `BREAKING CHANGE:` → Major version bump (1.0.0 → 2.0.0)

### 2. Release Process

When a new version is detected:

1. **Tests Run**: All tests must pass
2. **Linting**: Code quality checks
3. **Version Bump**: python-semantic-release determines new version
4. **Changelog Update**: CHANGELOG.md is automatically updated
5. **Git Tag**: A new tag is created (e.g., `v1.1.0`)
6. **PyPI Publish**: Package is published to PyPI
7. **GitHub Release**: Release notes are created on GitHub

## Setup Instructions

### 1. Initial Setup

Run the setup script to configure your repository:

```bash
# (Optional) helper script if present
./scripts/setup-release.sh || true
```

This will:
- Extract repository information from git
- Update all configuration files with correct URLs
- Set up proper author information

### 2. PyPI Token Setup

1. Go to [PyPI Account Settings](https://pypi.org/manage/account/)
2. Create an API token with "Upload packages" scope
3. Add it to GitHub Secrets:
   - Go to your repository settings
   - Navigate to "Secrets and variables" → "Actions"
   - Add new secret: `PYPI_API_TOKEN`

### 3. Git Configuration

Configure git to use conventional commit messages:

```bash
./setup-git.sh
```

## Commit Message Format

All commits must follow the [Conventional Commits](https://conventionalcommits.org/) specification:

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- `feat`: New features
- `fix`: Bug fixes
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `perf`: Performance improvements
- `test`: Test additions or changes
- `chore`: Build process or auxiliary tool changes

### Examples

```bash
# New feature
git commit -m "feat(mcp): add new search tools for financial data"

# Bug fix
git commit -m "fix(api): resolve authentication error in client"

# Documentation
git commit -m "docs: update installation instructions"

# Breaking change
git commit -m "feat(api): redesign client interface

BREAKING CHANGE: The client interface has been completely redesigned.
The old methods are no longer available."

# Multiple changes
git commit -m "feat(mcp): add new tools

- Add search tools for financial data
- Add chart tools for historical data
- Add company tools for profile information

Closes #123"
```

## Manual Testing

For comprehensive testing without using free tier minutes:

1. Go to the "Actions" tab in your GitHub repository
2. Select the "Test" workflow
3. Click "Run workflow"
4. Choose:
   - **Python version**: 3.8, 3.9, 3.10, 3.11, 3.12, or 3.13
   - **Test type**: all, unit, mcp, or integration
5. Click "Run workflow"

## Manual Release

If you need to trigger a release manually:

1. Go to the "Actions" tab in your GitHub repository
2. Select the "Release" workflow
3. Click "Run workflow"
4. Select the branch (usually `main`)
5. Click "Run workflow"

## Troubleshooting

### Common Issues

1. **Tests Failing**: Ensure all tests pass before pushing
2. **Linting Errors**: Run `uv run ruff check .` and `uv run ruff format .`
3. **PyPI Authentication**: Verify the `PYPI_API_TOKEN` secret is set correctly
4. **Version Not Bumping**: Check that commit messages follow conventional format and workflow ran on `main`

### Debug Commands

```bash
# Check commit messages
git log --oneline -10

# Run tests locally
uv run pytest tests/ -v

# Check linting
uv run ruff check .
uv run ruff format --check .

# Build package locally
uv build

# Test package installation
uv pip install dist/aiofmp-*.whl
```

### Release Notes

Release notes are automatically generated from commit messages and can be found in:

- `CHANGELOG.md` (in the repository)
- GitHub Releases (in the repository's releases section)

## Configuration Files

The release process uses several configuration files:

- `.github/workflows/release.yml`: GitHub Actions workflow
- `.github/workflows/test.yml`: Test workflow for PRs
- `pyproject.toml`: Python package & release configuration (contains [tool.semantic_release])
- `.gitmessage`: Git commit message template

## Best Practices

1. **Small, Focused Commits**: Make small, focused commits with clear messages
2. **Test Before Push**: Always run tests locally before pushing
3. **Conventional Commits**: Always use conventional commit format
4. **Breaking Changes**: Clearly mark breaking changes in commit messages
5. **Documentation**: Update documentation with new features
6. **Version Compatibility**: Consider backward compatibility when making changes

## Support

If you encounter issues with the release process:

1. Check the GitHub Actions logs
2. Verify all configuration files are correct
3. Ensure PyPI token has proper permissions
4. Check that commit messages follow conventional format
