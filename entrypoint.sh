#!/bin/sh

# Django-Initialisierung
echo "Applying database migrations..."
python manage.py makemigrations
python manage.py migrate --run-syncdb


echo "Seeding groups..."
python manage.py seedgroups

# Sammle statische Dateien
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Starte Gunicorn
echo "Starting Gunicorn..."
gunicorn StudurizerApp.wsgi:application --bind 0.0.0.0:8000 &

# Starte Nginx im Hintergrund
echo "Starting Nginx..."
nginx -g "daemon off;"

sleep 1