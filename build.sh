#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate

# Initialize data (runs every deploy, scripts are idempotent)
python create_subjects.py
python create_admin_on_deploy.py
