#!/bin/bash

# Script to check code formatting with ruff
# Usage: ./scripts/ruff_format_check.sh

set -e

echo "Checking code formatting with ruff..."
uv run ruff format .

echo "Checking code linting with ruff..."
uv run ruff check . --fix

echo "Running pre-commit hooks..."
pre-commit run --all-files

echo "Done!"
