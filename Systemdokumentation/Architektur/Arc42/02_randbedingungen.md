# 02 – Randbedingungen

In diesem Kapitel werden die nicht-funktionalen Anforderungen und technischen Rahmenbedingungen für das System „Studurizer“ beschrieben. Sie sind für Planung, Architektur und Entwicklung verbindlich.

## Technische Randbedingungen

- **Datenbank**: SQLite (leichtgewichtig, dateibasiert, geeignet für Prototyp und kleine bis mittlere Anwendungen)
- **Backend-Technologie**: Django (Python-basiertes Web-Framework, bewährt für schnelle Entwicklung und klare Architektur)
- **Frontend-Technologie**: HTML, CSS, JavaScript (Unter Verwendung von Fetch)
- **Containerisierung**: Docker (für reproduzierbare Entwicklungs- und Produktionsumgebungen, einfache Bereitstellung und Skalierbarkeit)
- **Server**: Lokale Ausführung und Deployment via Docker auf Linux-Server


## Organisatorische Randbedingungen

- **Benutzerverwaltung**: Registrierung ausschließlich durch Admins (Studierende und Dozierende erhalten ihre Zugangsdaten über die Administration)
- **Zugangskontrolle**: Rollensystem (Admin, Dozent:in, Student:in), spätere Erweiterung möglich
- **Barrierefreiheit**: Umsetzung gemäß **WCAG 2.2**
- **Datenschutz**: Berücksichtigung der DSGVO, Zusammenarbeit mit dem*der Datenschutzbeauftragten

## Rechtliche Randbedingungen

- **Datenschutz**: Einhaltung der DSGVO – insbesondere bzgl. personenbezogener Daten wie Name, ggf Matrikelnummer, Teilnahmeverläufe
- **Barrierefreiheit**: Verpflichtung zur Einhaltung barrierefreier Standards auf Grundlage öffentlicher Digitalangebote
- **Open-Source-Komponenten**: Es dürfen nur OSS-Komponenten verwendet werden, deren Lizenzen mit der Weiterverwendung vereinbar sind (z.B. MIT, Apache 2.0)

## Institutionelle Randbedingungen

- Projekt findet im Kontext einer Bildungseinrichtung statt
- Spätere Integration in bestehende Schulsysteme ist wünschenswert, aber nicht Teil der ersten Ausbaustufe
