#!/usr/bin/env bash
# Exit on error
set -o errexit

# Navigate into project folder
cd leave_system_final_copy

# Install dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt

# Run migrations and static files collection
python manage.py collectstatic --no-input
python manage.py migrate

# Automatically create superuser if environment variables are set
if [ "$DJANGO_SUPERUSER_USERNAME" ]; then
  python manage.py createsuperuser --no-input || true
fi
