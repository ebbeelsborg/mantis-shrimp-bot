#!/bin/sh

# Run Django migrations (SQLite for auth/sessions)
echo "Applying database migrations..."
python manage.py migrate

exec "$@"
