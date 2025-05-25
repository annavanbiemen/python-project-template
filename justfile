# Use the virtual environment
export PATH := justfile_directory() + '/.venv/bin:' + env('PATH')

# List targets by default
@_default:
    just --list --unsorted

# Sync the virtual environment
@_init:
    uv sync --quiet --frozen

# Shell into venv (!! experimental !!)
sh: _init
    #!/bin/bash
    bash --rcfile <(
        cat $HOME/.bashrc .venv/bin/activate;
        echo "alias deactivate=exit"
        for target in check fix test behave scan run
        do
            echo "alias $target='just $target'"
        done
    )

# Check code
check: _init
    ruff check
    ruff format --check
    pyright

# Fix code
fix: _init
    ruff check --fix-only
    ruff format

# Test for bugs
test: _init
    pytest

# Test behaviour
behave: _init
    behave

# Scan for vulnerabilities
scan: _init
    bandit -r src
    uv-secure

# Run the app
@run: _init
    app
