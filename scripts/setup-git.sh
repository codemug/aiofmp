#!/bin/bash

# Setup script for aiofmp development environment

echo "Setting up aiofmp development environment..."

# Configure git commit message template
git config commit.template .gitmessage

echo "✅ Git commit message template configured"
echo "✅ Development environment setup complete"
echo ""
echo "Next steps:"
echo "1. Update the repository URLs in pyproject.toml"
echo "2. Update author information in pyproject.toml"
echo "3. Set up PyPI API token in GitHub Secrets as PYPI_API_TOKEN"
echo "4. Push to GitHub and create your first release!"
