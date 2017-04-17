#!/bin/bash -xe

pycodestyle .
python tools/run-pyflakes.py
python tools/run-mccabe.py 10

pylint twittback
