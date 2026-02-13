#!/bin/sh

# Wait for postgres if needed (or rely on depends_on + retry logic in app)
# For simplicity in this demo, we'll just run migrations and then command

echo "Applying database migrations..."
python manage.py migrate

exec "$@"
