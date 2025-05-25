# Use the virtual environment
export PATH := justfile_directory() + '/.venv/bin:' + env('PATH')

# List commands
@_default:
    just --list --unsorted

# Check code
check:
    ruff check
    ruff format --check
    pyright

# Fix code
fix:
    ruff check --fix-only
    ruff format

# Test for bugs
test:
    pytest

# Test behaviour
behave:
    behave

# Scan for vulnerabilities
scan:
    bandit -r src
    uv-secure

# Run the app
@run:
    app
