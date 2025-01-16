#!/bin/sh

# Exit immediately if a command exits with a non-zero status
set -e

# Wait for database to be ready
echo "Waiting for PostgreSQL..."
while ! nc -z $DB_HOST $DB_PORT; do
  sleep 0.1
done
echo "PostgreSQL started"

# Run migrations
python manage.py migrate

# Create superuser if needed
python manage.py createsuperuser --noinput || true

# Collect static files
python manage.py collectstatic --noinput

# Start command
exec "$@"
