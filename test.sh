#!/bin/bash

mypy --ignore-missing-imports .
pep8 .
pylint -f colorized -r n electrode
python3 -m unittest discover
