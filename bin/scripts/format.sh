#!/bin/bash

isort  --line-length=90 src
yapf --in-place --recursive --style='{based_on_style: pep8, column_limit: 90}' src