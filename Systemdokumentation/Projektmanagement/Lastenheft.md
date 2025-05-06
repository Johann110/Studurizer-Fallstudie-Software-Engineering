<!---
Artefakte der Systemdokumentation wurden mithilfe von ChatGPT (OpenAI) erstellt und manuell angepasst
-->
# Lastenheft für das Projekt „Studurizer“

## 1. Einleitung

### 1.1 Ziel des Projekts
Ziel des Projekts „Studurizer“ ist die Entwicklung eines innovativen, barrierearmen Kursverwaltungssystems, das sich an etablierten Systemen wie MyCampus, Itslearning oder Iserv orientiert – jedoch mit einem stärkeren Fokus auf Barrierefreiheit und dem Einsatz neuer Technologien. Es wird als Webanwendung mit dem Framework Django realisiert.

### 1.2 Ausgangssituation
Viele bestehende Lern- und Kursplattformen bieten zwar umfassende Funktionen, weisen jedoch oft Defizite in der Barrierefreiheit, Benutzerfreundlichkeit oder technologischen Modernität auf. Besonders Studierende mit Einschränkungen stoßen häufig auf Hindernisse im digitalen Lernumfeld.

### 1.3 Zielgruppe
- Studierende (inkl. mit Behinderungen)
- Lehrende und Tutor:innen
- Hochschulverwaltung
- IT-Abteilungen
- Barrierefreiheitsbeauftragte
- Datenschutzbeauftragte
- Entwicklungsteam
- Externe KI-/Tool-Anbieter
---

## 2. Anforderungen

### 2.1 Funktionale Anforderungen
- Benutzer:innen (Studierende, Dozierende) werden ausschließlich durch Administratoren registriert
- Kurse können von Dozierenden erstellt und verwaltet werden
- Studierende können Kursen zugewiesen werden
- Kursmaterialien (Dateien, Videos, Links) können hochgeladen und verwaltet werden
- Kommunikation über Foren, Chats oder Kommentare
- Aufgaben-/Abgabe-Funktionen mit Deadlines
- Bewertungen für die Abgaben
- Rollensystem: Studierende, Lehrende, Admins
- Kalender-Integration mit Erinnerungsfunktion
- Barrierefreie Darstellung von Inhalten (Screenreader-Kompatibilität, Tastaturnavigation, Farbkontrast)
- Optional: Integration von KI-Tools (z.B. automatische Zusammenfassungen, Chatbot für Fragen)
- Erstellung von Zertifikaten (PDF)

### 2.2 Nicht-funktionale Anforderungen
- Webanwendung mit responsivem Design (Desktop, Tablet, Mobile)
- Einhaltung von WCAG-Richtlinien (Barrierefreiheit)
- DSGVO-Konformität
- Gute Performance bei vielen parallelen Nutzer:innen (>1000)
- Erweiterbarkeit durch Plugins oder Module
- Mehrsprachigkeit (mind. Deutsch und Englisch)
- Nutzung der SQLite-Datenbank für initiale Umsetzung (lokale Entwicklungsumgebung, einfache Wartung)

---

## 3. Rahmenbedingungen
- Technologiestack: Python (Django), HTML/CSS/JS, SQLite
- Open Source Frameworks bevorzugt
- Betrieb auf Linux-Servern der Hochschule oder lokal
- Entwicklungszeitraum: ca. 6 Monate
- Budget: studentisches Projekt, keine externen Dienstleister geplant

---

## 4. Abnahmekriterien
- Alle definierten Kernfunktionen müssen implementiert und getestet sein
- System läuft stabil im Testbetrieb mit realen Nutzer:innen
- WCAG-konforme Bedienung ist gewährleistet
- Feedback von Testgruppen (inkl. Menschen mit Behinderungen) fließt ein
- Dokumentation für Nutzer:innen und Admins liegt vollständig vor
- Datenschutzanforderungen gemäß DSGVO werden eingehalten