#!usr/bin/env bash
#exit on error
set -o errexit
pip install --upgrade pip gunicorn
pip install -r requirements.txt