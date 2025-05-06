<!---
Artefakte der Systemdokumentation wurden mithilfe von ChatGPT (OpenAI) erstellt und manuell angepasst
-->
# 04 – Lösungsstrategie

Dieses Kapitel beschreibt die grundlegenden Architektur- und Designentscheidungen für die Implementierung von Studurizer.

## Architekturmodell

Studurizer basiert auf einer klassischen **3-Schichten-Architektur**, bestehend aus:

1. **Präsentationsschicht**: HTML/CSS/JS mit Fokus auf Barrierefreiheit (WCAG 2.2)
2. **Applikationsschicht**: Django
3. **Datenhaltungsschicht**: SQLite-Datenbank

Diese Trennung erlaubt eine klare Strukturierung, gute Testbarkeit und zukünftige Erweiterbarkeit, z.B. durch mobile Clients oder andere Frontends.

## Technologiewahl

- **Backend**: Django (Python), inklusive Admin-Interface für Verwaltungsaufgaben
- **Frontend**: HTML5, CSS3, JavaScript 
- **Datenbank**: SQLite (lokal, dateibasiert, leichtgewichtig)
- **Containerisierung**: Docker zur Bereitstellung konsistenter Entwicklungs- und Deployment-Umgebungen

## Barrierefreiheit

- Umsetzung gemäß **WCAG 2.2**
- Unterstützung von Tastaturnavigation, Screenreadern, ausreichenden Kontrasten

## Sicherheit & Datenschutz

- Registrierung nur über Admins (keine öffentliche Registrierung)
- DSGVO-konforme Speicherung von Nutzerdaten
- Schutz sensibler Informationen durch Django-eigene Sicherheitsmechanismen
- Kommunikation über HTTPS (bei Deployment)

## Erweiterbarkeit

- Klare Modularisierung durch Django Apps (z.B. Kurse, Aufgaben, Kommunikation)
- Zukunf: Externe Services (z.B. KI-Tools) werden entkoppelt über APIs angebunden

## Entwicklungsstrategie

- Git-basierte Versionskontrolle
- CI/CD über GitHub Actions
- Entwicklungsnahe Tests durch Docker-Container (Dev/Staging)

