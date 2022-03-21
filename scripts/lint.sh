#!/bin/bash
set -e

SOURCES="linkcheck tests"

echo "Running isort..."
isort --check $SOURCES
echo "-----"

echo "Running black..."
black --skip-string-normalization --check $SOURCES
echo "-----"

echo "Running flake8..."
flake8 $SOURCES
echo "-----"

echo "Running mypy..."
mypy $SOURCES
echo "-----"

echo "All passed!"
