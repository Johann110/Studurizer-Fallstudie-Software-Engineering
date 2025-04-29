#!/bin/sh

# Django-Initialisierung
echo "Applying database migrations..."
python manage.py makemigrations
python manage.py migrate

echo "Seeding groups..."
python manage.py seedgroups

# Sammle statische Dateien
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Starte Nginx im Hintergrund
echo "Starting Nginx..."
nginx -g "daemon on;"

# Starte Gunicorn
echo "Starting Gunicorn..."
gunicorn studurizer.wsgi:application --bind 0.0.0.0:8000