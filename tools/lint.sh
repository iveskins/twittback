#!/bin/bash -xe

black --check .
python tools/run-pyflakes.py
python tools/run-mccabe.py 5
