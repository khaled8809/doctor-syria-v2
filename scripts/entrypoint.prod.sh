#!/bin/sh

# Get database host and port from DATABASE_URL
DB_HOST=$(echo $DATABASE_URL | sed -n 's/.*@\([^:]*\).*/\1/p')
DB_PORT=5432

# Wait for postgres
until nc -z $DB_HOST $DB_PORT; do
    echo "Waiting for postgres at $DB_HOST:$DB_PORT..."
    sleep 2
done

echo "PostgreSQL started"

# Run migrations
python manage.py migrate --no-input

# Collect static files
python manage.py collectstatic --no-input

# Create superuser if not exists
python manage.py createsuperuser --noinput || true

# Start the application
exec "$@"
