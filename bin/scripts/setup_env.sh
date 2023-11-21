#!/bin/bash

if [ ! -d "venv" ]; then
    python3.9 -m venv venv
fi

poetry export --without-hashes --dev -o dependencies.txt
venv/bin/pip install -r dependencies.txt
rm -f dependencies.txt
