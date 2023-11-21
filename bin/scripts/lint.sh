#!/bin/bash

LOGS="${1:-logs}"
FILES=$(find src -type f -name '*.py')

# Look into https://pypi.org/project/pylint-junit/
pylint --disable=logging-fstring-interpolation ${FILES}
# Currently crashes
# mypy --junit-xml=${LOGS}/mypy.xml ${FILES}
