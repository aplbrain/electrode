#!/bin/bash

mypy --ignore-missing-imports .
pylint -f colorized -r n electrode
nosetests --with-coverage --with-progressive --cover-package=electrode tests/
