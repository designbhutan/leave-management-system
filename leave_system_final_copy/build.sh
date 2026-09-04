#!/usr/bin/env bash
# Exit on error
set -o errexit

# Navigate to the folder containing manage.py and requirements.txt
cd leave_system_final_copy

# Upgrade pip and install dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt

# Run static assets collection and database migrations
python manage.py collectstatic --no-input
python manage.py migrate
