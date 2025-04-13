# Basis-Image
FROM python:3.10-slim

# Umgebungsvariablen setzen
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Arbeitsverzeichnis erstellen
RUN mkdir /app
WORKDIR /app

# Abhängigkeiten installieren
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Projekt-Dateien kopieren
COPY . /app/

# Port freigeben
EXPOSE 8000

# Startbefehl
RUN ["python", "manage.py", "makemigrations"]
RUN ["python", "manage.py", "migrate"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]