<!---
Artefakte der Systemdokumentation wurden mithilfe von ChatGPT (OpenAI) erstellt und manuell angepasst
-->
# 08 – Konzepte

Dieses Kapitel beschreibt zentrale Querschnittskonzepte, die unabhängig von einzelnen Modulen im gesamten System gelten.

---

## Sicherheitskonzept

- Registrierung ausschließlich durch Admins – kein Self-Signup
- Passwörter werden gehasht (Django default: PBKDF2)
- Zugriffskontrolle über Rollen (Student:in, Dozent:in, Admin)
- Middleware validiert Sessions oder Tokens bei jedem Request
- HTTPS ist für Deployment verpflichtend (via NGINX oder Cloud)

---

## Barrierefreiheitskonzept

- Umsetzung nach **WCAG 2.2** (neueste Version der Web Content Accessibility Guidelines)
- Anforderungen:
  - Screenreader-Kompatibilität
  - Tastaturnavigation ohne Maus
  - Kontraste > 4.5:1
  - Keine Inhalte ausschließlich durch Farbe vermittelt
  - Fokus-Indikatoren immer sichtbar

---

## Benutzer- und Rollenkonzept

- Benutzer werden in drei Rollen eingeteilt:
  - **Studierende**: passive Nutzer:innen, Zugriff auf Inhalte und Abgaben
  - **Dozierende**: erstellen und verwalten Kurse, Inhalte, Aufgaben
  - **Admin**: vollständiger Zugriff inkl. Benutzerverwaltung
- Jede Rolle hat eigene Views und Rechte innerhalb des Systems

---

## Persistenzkonzept

- Daten werden in SQLite gespeichert (für Prototyp und kleines Deployment)
- Modelle in Django basieren auf `models.Model` und sind modularisiert
- Dateien (z.B. Abgaben, Materialien) werden im lokalen Dateisystem gespeichert (MEDIA_ROOT)
- Optionale Erweiterung: Persistenzschicht via PostgreSQL oder Cloud-Speicher

---

## Fehlermanagement

- Serverseitige Fehler (500, 404) werden über eigene Templates mit verständlicher UX dargestellt
- Logging erfolgt über Djangos Logging-System in Datei + Konsole
- Fehlermeldungen an Benutzer:innen sind barrierefrei und verständlich formuliert
- Backend prüft Eingaben serverseitig, zusätzlich zu Frontend-Validierungen

---

## Benachrichtigungskonzept

- Wichtige Aktionen (z. B. Kursanmeldung, Abgabeerinnerung) erzeugen E-Mail-Benachrichtigungen
- In Entwicklung: Fake-Mailer oder Konsole
- In Produktion: Anbindung an SMTP-Relay (z.B. über Hochschule)

---
