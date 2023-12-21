#!/bin/bash

# Check if 'python' command is available
if command -v python &>/dev/null; then
    PYTHON_CMD=python
# Check if 'python3' command is available
elif command -v python3 &>/dev/null; then
    PYTHON_CMD=python3
else
    echo "Python is not installed."
    exit 1
fi

$PYTHON_CMD -m unittest discover -s tests/
