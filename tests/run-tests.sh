#!/usr/bin/env bash

pip install --upgrade pip
pip install poetry
poetry update

set -e

export PYTHONPATH=$(pwd)
poetry run py.test -v -s --cov=love_letter --cov-report term tests
poetry run behave
