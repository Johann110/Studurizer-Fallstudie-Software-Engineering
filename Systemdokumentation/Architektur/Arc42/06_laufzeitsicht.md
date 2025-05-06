<!---
Artefakte der Systemdokumentation wurden mithilfe von ChatGPT (OpenAI) erstellt und manuell angepasst
-->
# 06 – Laufzeitsicht

Dieses Kapitel zeigt das dynamische Verhalten des Systems anhand exemplarischer Szenarien.

## 1. Login eines Studierenden

Beim Login werden die Zugangsdaten überprüft, ein Token oder Session-Cookie erstellt und der Nutzer weitergeleitet.

```mermaid
sequenceDiagram
    participant Browser
    participant Frontend
    participant Backend (accounts)
    participant DB

    Browser->>Frontend: Login-Formular ausfüllen
    Frontend->>Backend (accounts): POST /login (E-Mail, Passwort)
    Backend (accounts)->>DB: Anfrage: Nutzer mit E-Mail + Passwort-Hash
    DB-->>Backend (accounts): Benutzer gefunden
    Backend (accounts)-->>Frontend: Session-Cookie / Token
    Frontend-->>Browser: Weiterleitung zum Dashboard
```
## 2. Erstellung von Kursen
```mermaid
sequenceDiagram
    participant Dozierender
    participant Frontend
    participant Backend (courses)
    participant DB

    Dozierender->>Frontend: Formular „Neuer Kurs“
    Frontend->>Backend (courses): POST /courses/create (Titel, Beschreibung, Zeitraum)
    Backend (courses)->>DB: INSERT neuer Kurs
    DB-->>Backend (courses): Bestätigung
    Backend (courses)-->>Frontend: Erfolgs-Response
    Frontend-->>Dozierender: Kursübersicht aktualisiert
```

## 3. Erstellung von Terminen
```mermaid
sequenceDiagram
    participant Dozierender
    participant Frontend
    participant Backend (courses)
    participant DB

    Dozierender->>Frontend: Terminformular ausfüllen
    Frontend->>Backend (courses): POST /courses/<kurs-id>/schedule
    Backend (courses)->>DB: Speichere Termin zu Kurs
    DB-->>Backend (courses): OK
    Backend (courses)-->>Frontend: Erfolgs-Response
    Frontend-->>Dozierender: Anzeige aktualisiert
```
## 4. Erstellung von Abgaben
```mermaid
sequenceDiagram
    participant Studierender
    participant Frontend
    participant Backend (assignments)
    participant DB
    participant FileSystem

    Studierender->>Frontend: Datei auswählen + Aufgabe abschicken
    Frontend->>Backend (assignments): POST /assignments/submit (Datei + Metadaten)
    Backend (assignments)->>FileSystem: Datei speichern
    Backend (assignments)->>DB: Speichere Abgabe-Referenz
    DB-->>Backend (assignments): OK
    Backend (assignments)-->>Frontend: Erfolg / Feedback
    Frontend-->>Studierender: Anzeige aktualisiert („Erfolgreich eingereicht“)

```
## 5. Korrektur von Abgaben
```mermaid
sequenceDiagram
    participant Dozierender
    participant Frontend
    participant Backend (assignments)
    participant DB

    Dozierender->>Frontend: Bewertung öffnen
    Frontend->>Backend (assignments): GET /assignments/<abgabe-id>
    Backend (assignments)->>DB: Lade Abgabe + Metadaten
    DB-->>Backend (assignments): Abgabe-Daten
    Backend (assignments)-->>Frontend: Rückgabe Bewertungseinheit
    Dozierender->>Frontend: Bewertung eingeben
    Frontend->>Backend (assignments): POST /assignments/<abgabe-id>/grade
    Backend (assignments)->>DB: Speichere Bewertung
    DB-->>Backend (assignments): OK
    Backend (assignments)-->>Frontend: Bewertung erfolgreich gespeichert
```