#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "Running migrations..."
python manage.py migrate --noinput

echo "Seeding database..."
# Uncomment the line below to seed database on startup
# python manage.py seed_data

echo "Starting Gunicorn server..."
exec gunicorn pharmacy_project.wsgi:application --bind 0.0.0.0:8000
