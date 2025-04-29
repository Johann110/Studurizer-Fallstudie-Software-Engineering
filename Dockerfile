# Basis-Image
FROM python:3.11-slim

# Umgebungsvariablen setzen
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Nginx installieren
RUN apt-get update && \
    apt-get install -y nginx && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Arbeitsverzeichnis erstellen
RUN mkdir /app
WORKDIR /app

# Abhängigkeiten installieren
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Nginx-Konfiguration
COPY nginx.conf /etc/nginx/sites-available/default
RUN ln -sf /etc/nginx/sites-available/default /etc/nginx/sites-enabled/default

# Projekt-Dateien kopieren
COPY . /app/

# Beide Ports freigeben (Nginx und Gunicorn)
EXPOSE 80

# Führe entrypoint.sh aus
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh
CMD ["/app/entrypoint.sh"]