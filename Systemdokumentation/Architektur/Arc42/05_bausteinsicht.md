<!---
Artefakte der Systemdokumentation wurden mithilfe von ChatGPT (OpenAI) erstellt und manuell angepasst
-->
# 05 – Bausteinsicht

Diese Bausteinsicht beschreibt die statische Struktur von Studurizer.  
Das System ist in mehrere logisch und fachlich getrennte Module (Django Apps) unterteilt.

## Übersicht über Systembausteine

Studurizer folgt einer modularen Micro - Service Struktur nach dem Django-Framework-Prinzip. Die wichtigsten Module sind:

| Modul             | Beschreibung                                                                     |
|-------------------|----------------------------------------------------------------------------------|
| **accounts**      | Verwaltung von Benutzer:innen, Rollen, Authentifizierung                         |
| **courses**       | Erstellung und Verwaltung von Kursen, Zuweisung von Teilnehmenden                |
| **events**        | Erstellung und Verwaltung von Terminen                                           |
| **documents**     | Upload, Download und Versionierung von Lernmaterialien                           |
| **assignments**   | Erstellung von Leistungskontrollen                                               |
| **submissions**   | Ermöglicht das einreichen von Abgaben für Leistungskontrollen                    |
| **grades**        | Ermöglicht das bewerten von Abgaben                                              |
| **certificates**  | Erstellung von PDF Zertifikaten für Schüler/Studenten u. Versand via Email       |
| **admin**         | Sonderfunktionen für Admins, abgewickelt durch Django (z.B. Nutzerregistrierung) |
| **StudurizerApp** | Funktionenbuendlung, Konfiguration, Hauptrouting, Sicherheit, Logging            |

---

## Strukturdiagramm (Mermaid)

```mermaid
graph TD
    A[StudurizerApp] --> B[accounts]
    A --> F[events]
    A --> C[courses]
    C --- F
    C --> D[documents]
    C --> E[assignments]
    H[submissions] --> E
    I[grades] --> H
    J[certificates] --> I
    A --> G[adminpanel]
