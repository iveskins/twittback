#!/bin/bash -xe

pycodestyle .
python tools/run-pyflakes.py
python tools/run-mccabe.py 5

pylint twittback --score=no
