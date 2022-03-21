#!/bin/bash
SOURCES="linkcheck tests"

echo "Running isort..."
isort $SOURCES
echo "-----"

echo "Running black..."
black --skip-string-normalization $SOURCES
