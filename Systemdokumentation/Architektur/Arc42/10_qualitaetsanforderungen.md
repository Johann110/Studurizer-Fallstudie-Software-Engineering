<!---
Artefakte der Systemdokumentation wurden mithilfe von ChatGPT (OpenAI) erstellt und manuell angepasst
-->
# 10 – Qualitätsanforderungen

Dieses Kapitel beschreibt die nicht-funktionalen Anforderungen an das System Studurizer. Die Ziele orientieren sich an den Qualitätsattributen nach ISO/IEC 25010.

---

## Testbarkeit

- Für alle **CRUD-Funktionen** (Create, Read, Update, Delete) muss eine **automatisierte Testabdeckung** vorhanden sein.
- Es werden vorrangig **Unit- und Integrationstests** geschrieben.
- **E2E-Tests (End-to-End)** gelten im Projektkontext als nachrangig und sind nicht verpflichtend.

---

## Verständlichkeit und Clean Code

- Der Quellcode soll **selbsterklärend** und gut strukturiert sein.
- **Kommentare sind sparsam** und nur bei wirklich komplexer Logik zu verwenden.
- Die **Benennung von Funktionen, Variablen und Klassen** erfolgt sprechend nach Best Practices (PEP8).
- Die interne Architektur ist möglichst flach, übersichtlich und modular.

---

## Barrierefreiheit

- Das System muss den **Richtlinien der WCAG 2.2** entsprechen.
- Es werden regelmäßig manuelle Tests mit Screenreadern und Tastaturnavigation durchgeführt.
- Farbgestaltung und Kontraste werden geprüft.

---

## Sicherheit

- Passwörter werden gehasht (Django-Standard: PBKDF2).
- Zugriff auf sensible Bereiche erfolgt rollenbasiert.
- Eingaben werden validiert (Frontend & Backend).
- Keine öffentlich zugängliche Registrierung.

---

## Benutzerfreundlichkeit

- Die Benutzeroberfläche soll **intuitiv und modern** sein („Flashy UI“) ohne Barrierefreiheit zu beeinträchtigen.
- Reduktion auf das Wesentliche bei Seitenlayout und Interaktion.
- Responsives Design (Desktop und mobil bedienbar).

---

## Wartbarkeit

- Modularer Aufbau in Form einzelner Django-Apps
- Leicht verständliche Projektstruktur
- Dockerisierung für reproduzierbare Entwicklungs- und Testumgebungen
