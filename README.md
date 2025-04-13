# MyCampus-Learn-Fallstudie-Software-Engineering

# Docker für Studurizer

Diese Anleitung erklärt, wie du das Studurizer-Projekt mit Docker lokal ausführen kannst.

## Voraussetzungen

- [Git](https://git-scm.com/downloads) installiert
- [Docker](https://docs.docker.com/get-docker/) installiert
- [Docker Compose](https://docs.docker.com/compose/install/) installiert (in den meisten Docker-Desktop-Installationen bereits enthalten)

## Installationsschritte

1. **Repository klonen**

   ```bash
   git clone https://github.com/Johann110/Studurizer-Fallstudie-Software-Engineering.git
   cd studurizer
   ```

2. **Verzeichnisstruktur prüfen**

   Stelle sicher, dass die folgenden Verzeichnisse/Dateien vorhanden sind oder erstelle sie:
   ```bash
   # Verzeichnis für Medien-Dateien
   mkdir -p media
   
   # Stelle sicher, dass die db existiert
   touch db.sqlite3
   ```

3. **Docker Image bauen**

   ```bash
   docker compose build
   ```

4. **compose.yaml anpassen**

   Passe die compose.yaml Datei an und setze die Umgebungsvariablen


5. **Container starten**

   ```bash
   # Container starten
   docker compose up
   ```

5. **Admin-Benutzer erstellen**

   Öffne ein neues Terminal-Fenster und führe aus:
   ```bash
   docker compose exec studurizer python manage.py createsuperuser
   ```

6. **Zugriff auf die Anwendung**

   Öffne deinen Webbrowser und gehe zu: http://localhost:8000

## Dateipfade und Persistenz

Die Docker-Konfiguration verwendet zwei wichtige Volumes:

- **Mediendateien (`./media:/app/media`)**: Hochgeladene Dateien (z.B. Profilbilder, Kursunterlagen) werden im `media`-Verzeichnis gespeichert.

- **Datenbank (`./db.sqlite3:/app/db.sqlite3`)**: Die SQLite-Datenbank wird direkt im Projektverzeichnis gespeichert und bleibt auch nach dem Neustart des Containers erhalten.

## Häufig verwendete Befehle

### Container im Hintergrund starten
```bash
docker compose up -d
```

### Container stoppen
```bash
docker compose down
```

### Logs anzeigen
```bash
docker compose logs
```

### Django-Management-Befehle ausführen
```bash
docker compose exec studurizer python manage.py [befehl]
```

## Fehlerbehebung

### Container startet nicht
Überprüfe die Logs:
```bash
docker compose logs
```

### Datenbank-Probleme
Wenn es Probleme mit der Datenbank gibt, kannst du versuchen, die Migrationen erneut anzuwenden:
```bash
docker compose exec studurizer python manage.py migrate
```

### Probleme mit Dateiberechtigungen
Wenn Berechtigungsprobleme mit den gemounteten Volumes auftreten:
```bash
# Unter Linux/macOS: Setze Berechtigungen für das media-Verzeichnis
sudo chmod -R 777 media

# Oder ändere den Besitzer auf deinen Benutzer
sudo chown -R $(whoami):$(whoami) media db.sqlite3
```