#!/bin/bash

COVERAGE_THRESHOLD=80
coverage run -m unittest discover -s tests/
COVERAGE_PERCENTAGE=$(coverage report -m | grep TOTAL | awk '{print $4}' | tr -d %)
echo "Test coverage: ${COVERAGE_PERCENTAGE}%"
if [ "${COVERAGE_PERCENTAGE}" -lt "${COVERAGE_THRESHOLD}" ]; then
    echo "Error: Test coverage is below the required threshold of ${COVERAGE_THRESHOLD}%"
    exit 1
fi
