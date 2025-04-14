# 05 – Bausteinsicht

Diese Bausteinsicht beschreibt die statische Struktur von Studurizer.  
Das System ist in mehrere logisch und fachlich getrennte Module (Django Apps) unterteilt.

## Übersicht über Systembausteine

Studurizer folgt einer modularen Micro - Service Struktur nach dem Django-Framework-Prinzip. Die wichtigsten Module sind:

| Modul             | Beschreibung                                                                      |
|-------------------|-----------------------------------------------------------------------------------|
| **accounts**      | Verwaltung von Benutzer:innen, Rollen, Authentifizierung                          |
| **courses**       | Erstellung und Verwaltung von Kursen, Zuweisung von Teilnehmenden, Termine        |
| **documents**     | Upload, Download und Versionierung von Lernmaterialien                            |
| **assignments**   | Aufgabenstellungen, Abgaben und Bewertungen                                       |
| **admin**         | Sonderfunktionen für Admins, abgewickelt durch Django (z. B. Nutzerregistrierung) |
| **StudurizerApp** | Funktionenbuendlung, Konfiguration, Hauptrouting, Sicherheit, Logging             |

---

## Strukturdiagramm (Mermaid)

```mermaid
graph TD
    A[core] --> B[accounts]
    A --> C[courses]
    C --> D[documents]
    C --> E[assignments]
    A --> G[adminpanel]
