<!---
Artefakte der Systemdokumentation wurden mithilfe von ChatGPT (OpenAI) erstellt und manuell angepasst
-->
# Pflichtenheft für die Lernplattform „Studurizer"
## 1. Einleitung
### 1.1 Ziel des Dokuments
Dieses Pflichtenheft beschreibt die konkrete technische Umsetzung der Anforderungen aus dem Lastenheft für die Lernplattform „Studurizer".
"Ziel des Projekts „Studurizer“ ist die Entwicklung eines innovativen, barrierearmen Kursverwaltungssystems, das sich an etablierten Systemen wie MyCampus, Itslearning oder Iserv orientiert – jedoch mit einem stärkeren Fokus auf Barrierefreiheit und dem Einsatz neuer Technologien. Es wird als Webanwendung mit dem Framework Django realisiert."

### 1.2 Verantwortlichkeiten

- Auftraggeber: Bildungsinstitutionen
- Auftragnehmer: Study4U
- Projektleitung: Marvin Hamacher

## 2. Systemübersicht
„Studurizer“ ist eine Webanwendung, die mit dem Django-Framework (Python) entwickelt wird.
Für das Frontend werden HTML, CSS und JavaScript genutzt. Die Datenhaltung erfolgt über eine SQLite-Datenbank.
Der Fokus liegt auf intuitiver Benutzerführung, Barrierefreiheit und Erweiterbarkeit.

## 3. Technische Umsetzung der Anforderungen
### 3.1 Funktionale Anforderungen und deren Umsetzung
| Modul             | Beschreibung                                                                     |
| ----------------- | -------------------------------------------------------------------------------- |
| **accounts**      | Verwaltung von Benutzer:innen, Rollen, Authentifizierung                         |
| **courses**       | Erstellung und Verwaltung von Kursen, Zuweisung von Teilnehmenden                |
| **events**        | Verwaltung von Vorlesungsterminen und sonstigen Veranstaltungen                  |
| **documents**     | Upload, Download und Versionierung von Lernmaterialien                           |
| **assignments**   | Erstellung von Leistungskontrollen (ohne Bewertungskriterien, aber Anhang möglich) |
| **submissions**   | Ermöglicht das Einreichen von Abgaben für Leistungskontrollen                    |
| **grades**        | Ermöglicht das Bewerten von Abgaben                                              |
| **certificates**  | Erstellung von PDF-Zertifikaten für Schüler/Studenten und Versand via E-Mail     |
| **admin**         | Sonderfunktionen für Admins, abgewickelt durch Django (z.B. Nutzerregistrierung) |
| **StudurizerApp** | Funktionenbündelung, Konfiguration, Hauptrouting, Sicherheit, Logging            |

### 3.2 Nicht-funktionale Anforderungen und deren Umsetzung

| Anforderung       | Umsetzung                                                  |
| ----------------- | ---------------------------------------------------------- |
| Barrierefreiheit  | Umsetzung von Kontrasten, ARIA-Labels, Tastatur-Navigation |
| Modularität       | Trennung in Django-Apps, lose Kopplung                     |
| Datenspeicherung  | SQLite für schnelle Entwicklung und einfache Wartung       |
| Sicherheit        | CSRF-Schutz, Passwort-Hashing, Rechteverwaltung            |
| Erweiterbarkeit   | Nutzung von Django Best Practices, Modulare Architektur    |
| Responsive Design | Bootstrap/Custom CSS, Mobile First                         |

## 4. Architektur und Systemdesign

### 4.1 Systemkomponenten

* **Backend:** Django (Python)
* **Datenbank:** SQLite
* **Frontend:** HTML, CSS, JavaScript
* **PDF-Generierung:** xhtml2pdf
* **E-Mail-Versand:** Google

### 4.2 Beispielhafte Datenbankstruktur (Auszug)

#### Tabelle: courses

| id | title        | description          | start_date | end_date   |
| -- | ------------ | -------------------- |------------|------------|
| 1  | Informatik 1 | Einführung in Python | 2025-05-20 | 2025-05-24 |

## 5. Testfälle und Abnahme

### 5.1 Testfälle

* **Funktionstest:** Kurs erstellen, Benutzer registrieren, Rollen vergeben, Termin anlegen
* **Responsivitätstest:** Darstellung auf BESTIMMTEN Geräten

### 5.2 Abnahmekriterien

* Alle Kernfunktionen gemäß Lastenheft funktionieren fehlerfrei.
* Das System erfüllt Anforderungen an Barrierefreiheit und Benutzerfreundlichkeit.
* Tests verlaufen erfolgreich, inkl. PDF- und E-Mail-Funktionen.

## 6. Zeit- und Ressourcenplanung

### 6.1 Zeitplan

| Phase          | Zeitraum |
| -------------- |----------|
| Planung        | 1 Woche  |
| Umsetzung      | 3 Wochen |
| Test & Abnahme | 1 Woche  |

### 6.2 Ressourcen

* 3 Entwickler\:innen (2 Richtung Django Fullstack, 1 Richtung Container u. Deployment)

---

Letzte Aktualisierung: 06. Mai 2025
