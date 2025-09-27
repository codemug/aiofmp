#!/bin/bash

# Setup script for aiofmp release configuration

set -e

echo "🚀 Setting up aiofmp for automated releases..."

# Check if we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "❌ Error: Not in a git repository"
    exit 1
fi

# Get repository information
REPO_URL=$(git config --get remote.origin.url)
if [ -z "$REPO_URL" ]; then
    echo "❌ Error: No remote origin found"
    exit 1
fi

# Extract repository name and owner
if [[ $REPO_URL =~ github\.com[:/]([^/]+)/([^/]+) ]]; then
    OWNER="${BASH_REMATCH[1]}"
    REPO="${BASH_REMATCH[2]%.git}"
else
    echo "❌ Error: Could not extract repository information from $REPO_URL"
    exit 1
fi

echo "📦 Repository: $OWNER/$REPO"

# Update pyproject.toml
echo "📝 Updating pyproject.toml..."
sed -i.bak "s|https://github.com/your-username/aiofmp|https://github.com/$OWNER/$REPO|g" pyproject.toml
sed -i.bak "s|Your Name|$OWNER|g" pyproject.toml
sed -i.bak "s|your.email@example.com|$OWNER@users.noreply.github.com|g" pyproject.toml

# Update package.json
echo "📝 Updating package.json..."
sed -i.bak "s|https://github.com/your-username/aiofmp|https://github.com/$OWNER/$REPO|g" package.json
sed -i.bak "s|Your Name|$OWNER|g" package.json
sed -i.bak "s|your.email@example.com|$OWNER@users.noreply.github.com|g" package.json

# Update .releaserc.json
echo "📝 Updating .releaserc.json..."
sed -i.bak "s|https://github.com/your-username/aiofmp.git|https://github.com/$OWNER/$REPO.git|g" .releaserc.json

# Clean up backup files
rm -f pyproject.toml.bak package.json.bak .releaserc.json.bak

echo "✅ Configuration updated successfully!"
echo ""
echo "🔧 Next steps:"
echo "1. Set up PyPI API token in GitHub Secrets:"
echo "   - Go to https://pypi.org/manage/account/"
echo "   - Create an API token"
echo "   - Add it to GitHub Secrets as PYPI_API_TOKEN"
echo ""
echo "2. Configure git commit message template:"
echo "   ./scripts/setup-git.sh"
echo ""
echo "3. Make your first commit and push:"
echo "   git add ."
echo "   git commit -m 'chore: setup automated releases'"
echo "   git push origin main"
echo ""
echo "🎉 Your automated release pipeline is ready!"
