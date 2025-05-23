<!---
Artefakte der Systemdokumentation wurden mithilfe von ChatGPT (OpenAI) erstellt und manuell angepasst
-->
## MyCampus-Learn-Fallstudie-Software-Engineering

## Angaben zur Drittanbieter-Software

Alle Quellen, Lizenzen und Copyrightangaben für verwendete Software befinden sich in der Datei CREDITS.md im Hauptverzeichnis.

## Hinweis zum KI-Einsatz

Teile des Codes in diesem Projekt wurden mithilfe von KI-Tools wie ChatGPT (OpenAI), Grok, Claude AI (Anthropic) und GitHub Copilot generiert oder überarbeitet. Alle generierten Inhalte wurden manuell überprüft und angepasst.
 
# Docker für Studurizer

Diese Anleitung erklärt, wie du das Studurizer-Projekt mit Docker lokal ausführen kannst.

## Voraussetzungen

- [Docker](https://docs.docker.com/get-docker/) installiert
- [Docker Compose](https://docs.docker.com/compose/install/) installiert (in den meisten Docker-Desktop-Installationen bereits enthalten)

## Installationsschritte

1. **Verzeichnis erstellen und Struktur prüfen**

   Stelle sicher, dass die folgenden Verzeichnisse/Dateien vorhanden sind oder erstelle sie:
   ```bash
   # Ordner für die App erstellen und in den Pfad
   mkdir studurizer
   cd studurizer
   
   # Verzeichnis für Medien-Dateien und Datenbank erstellen
   mkdir -p media data
   ```

2. **Compose-Datei erstellen und Container starten**

   Erstelle eine `compose.yaml` mit folgendem Inhalt oder lade die [example.compose.yaml herunter](https://github.com/Johann110/Studurizer-Fallstudie-Software-Engineering/raw/refs/heads/main/example.compose.yaml) und passe die Umgebungsvariablen an:

   ```yaml
   services:
     studurizer:
       container_name: studurizer
       image: ghcr.io/johann110/studurizer-fallstudie-software-engineering:latest
       ports:
         - "80:80"  # Exponiert Port 80
       volumes:
         - ./data:/app/data # Pfad zur lokalen SQLite-Datenbank (links anpassen, falls nötig)
         - ./media:/app/media            # Ordner für Medien-Dateien (links anpassen, falls nötig)
       environment:
         - SECRET_KEY=${SECRET_KEY:-default_development_key}  # SECRET_KEY generieren: https://djecrety.ir oder z. B. python -c "import secrets; print(secrets.token_urlsafe(50))"
   #      - DOMAIN=${DOMAIN:-DOMAIN} # Domain setzen wenn SSL benutzt wird oder eine Domain um auf die App zugreifen (optional)
   #      E-Mails sind optional, diese werden genutzt um E-Mails an Nutzer zu senden (z.B. Zertifikate oder Informationen)
   #      - SMTP_USERNAME=user@gmail.com # Username für den SMTP Server
   #      - SMTP_PASSWORD=myapppassword     # SMTP Passwort
   #      - SMTP_SERVER=smtp.gmail.com         # SMTP Server
   #      - SMTP_PORT=587                      # SMTP Port
   #      - SMTP_DOMAIN=gmail.com              # Domäne der E-Mail Domain @domain.com
   #      - USE_SSL=False                      # SSL benutzen wenn StarTLS nicht geht / Default False
   #      - USE_STARTLS=True                   # StarTLS benutzen / Default True
   ```

   Container starten:

      ```bash
      docker compose up
      ```

3. **Admin-Benutzer erstellen**

   Öffne ein neues Terminal-Fenster und führe aus:
   ```bash
   docker compose exec studurizer python manage.py createsuperuser
   ```

4. **Zugriff auf die Anwendung**

   Öffne deinen Webbrowser und gehe zu: http://localhost:80

## Dateipfade und Persistenz

Die Docker-Konfiguration verwendet zwei wichtige Volumes:

- **Mediendateien (`./media:/app/media`)**: Hochgeladene Dateien (z.B. Profilbilder, Kursunterlagen) werden im `media`-Verzeichnis gespeichert.

- **Datenbank (`./data:/app/data`)**: Die SQLite-Datenbank wird direkt im Data Verzeichnis gespeichert und bleibt auch nach dem Neustart des Containers erhalten.

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
