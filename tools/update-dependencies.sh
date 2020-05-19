#!/bin/bash
set -euo pipefail

pipenv install
pipenv run pipenv-setup sync
pipenv run pipenv-setup sync --dev
