#!/bin/bash
export FLASK_APP=test.py
HOST="0.0.0.0"
PORT="81"
echo "starting webfrontend on ${HOST}:${PORT}"

python -m flask run --host=${HOST} --port=${PORT}
