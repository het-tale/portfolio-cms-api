#! /usr/bin/env bash

export PYTHONPATH=.
# This script is run before the application starts to ensure that the database is initialized with initial data.

python3 app/initial_data.py 