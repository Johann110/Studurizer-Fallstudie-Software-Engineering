# Basis-Image
FROM python:3.11-slim

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

# Führe entrypoint.sh aus
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh
CMD ["/app/entrypoint.sh"]