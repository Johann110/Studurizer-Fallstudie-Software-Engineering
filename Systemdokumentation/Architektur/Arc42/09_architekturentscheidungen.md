# 09 – Architekturentscheidungen

Dieses Kapitel dokumentiert wesentliche Architekturentscheidungen, die im Projektverlauf getroffen wurden.

---

## Entscheidung 1: Nutzung von Django als Web-Framework

- **Datum**: 2025-04-08  
- **Status**: angenommen

**Kontext / Problem**  
Für die Umsetzung eines serverseitigen Web-Backends wird ein Framework benötigt, das schnell produktiv ist und ein stabiles Ökosystem bietet.

**Entscheidung**  
Das Framework **Django (Python)** wird als Basis für die Backend-Logik und Datenmodellierung eingesetzt.

**Begründung**  
- Sehr gut geeignet für CRUD-Anwendungen
- Integrierte Admin-Oberfläche für Admin-Zugriffe
- Gute Dokumentation und Community
- Schnelle Entwicklungszyklen durch hohe Abstraktion

**Alternativen**  
- Flask (leichter, aber weniger strukturiert)
- Node.js mit Express (JavaScript-basierte Lösung)

**Auswirkungen**  
- Python als Projektsprache gesetzt
- Struktur und Modularisierung durch Django-Apps vorgegeben

---

## Entscheidung 2: Benutzer werden ausschließlich durch Admins registriert

- **Datum**: 2025-04-08  
- **Status**: angenommen

**Kontext / Problem**  
Öffentliche Registrierung durch Benutzer:innen ist aus Datenschutz- und Kontrollgründen nicht gewünscht.

**Entscheidung**  
Nur Administrator:innen können Benutzer:innen (Studierende und Dozierende) im System registrieren. 
Wie es in Schulen eben üblich ist.

**Begründung**  
- Höhere Kontrolle über Benutzeridentitäten
- Erleichtert DSGVO-konforme Verwaltung
- Vereinfachung des Login-Prozesses

**Alternativen**  
- Selbstregistrierung mit E-Mail-Bestätigung

**Auswirkungen**  
- Benutzer:innen sind auf Admins angewiesen
- Admin-Oberfläche muss erweiterte Benutzerpflege bereitstellen

---

## Entscheidung 3: Verwendung von SQLite in der ersten Ausbaustufe

- **Datum**: 2025-04-08  
- **Status**: angenommen

**Kontext / Problem**  
Für den Prototypen wird eine einfache, wartungsarme Datenbank benötigt, die lokal schnell eingerichtet ist.

**Entscheidung**  
SQLite wird als initiale Datenbanklösung verwendet.

**Begründung**  
- Kein Setup notwendig, läuft direkt in Django
- Für kleine/mittlere Nutzerzahlen performant genug
- Leichtgewichtig und portabel

**Alternativen**  
- PostgreSQL (produktionsreif, aber komplexer im Setup)

**Auswirkungen**  
- Datenbank ist dateibasiert und nicht für parallele Zugriffe bei hoher Last geeignet
- Leichter Umstieg auf PostgreSQL durch ORM möglich

