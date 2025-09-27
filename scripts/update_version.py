#!/usr/bin/env python3
"""
Script to update version in pyproject.toml and package.json for semantic-release
"""
import sys
import re
import json
from pathlib import Path


def update_pyproject_version(new_version: str) -> None:
    """Update version in pyproject.toml"""
    pyproject_path = Path("pyproject.toml")
    
    if not pyproject_path.exists():
        print("Error: pyproject.toml not found", file=sys.stderr)
        return False
    
    # Read the current content
    content = pyproject_path.read_text()
    
    # Update only the project version (first occurrence after [project])
    # More specific pattern to only match the project version
    pattern = r'(\[project\].*?\n)version\s*=\s*"[^"]*"'
    replacement = rf'\1version = "{new_version}"'
    
    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    if new_content == content:
        # Fallback to simpler pattern if the above doesn't work
        pattern = r'^version\s*=\s*"[^"]*"'
        replacement = f'version = "{new_version}"'
        new_content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
    
    if new_content == content:
        print("Warning: Version pattern not found in pyproject.toml", file=sys.stderr)
        return False
    
    # Write back the updated content
    pyproject_path.write_text(new_content)
    print(f"Updated version to {new_version} in pyproject.toml")
    return True


def update_package_json_version(new_version: str) -> None:
    """Update version in package.json if it exists"""
    package_json_path = Path("package.json")
    
    if not package_json_path.exists():
        print("package.json not found, skipping")
        return True
    
    try:
        # Read and parse package.json
        with open(package_json_path, 'r') as f:
            data = json.load(f)
        
        # Update version
        data['version'] = new_version
        
        # Write back with proper formatting
        with open(package_json_path, 'w') as f:
            json.dump(data, f, indent=2)
            f.write('\n')  # Add trailing newline
        
        print(f"Updated version to {new_version} in package.json")
        return True
        
    except (json.JSONDecodeError, KeyError, IOError) as e:
        print(f"Error updating package.json: {e}", file=sys.stderr)
        return False


def update_version(new_version: str) -> None:
    """Update version in both pyproject.toml and package.json"""
    success = True
    
    success &= update_pyproject_version(new_version)
    success &= update_package_json_version(new_version)
    
    if not success:
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python update_version.py <new_version>", file=sys.stderr)
        sys.exit(1)
    
    new_version = sys.argv[1]
    update_version(new_version)