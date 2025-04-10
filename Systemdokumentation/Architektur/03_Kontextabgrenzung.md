# 03 – Kontextabgrenzung

## Fachlicher Kontext

Das System „Studurizer“ ist eine Webplattform zur Kursverwaltung an Hochschulen. Es dient der Verwaltung von Lehrveranstaltungen, Kursmaterialien, Teilnehmendenlisten und Aufgaben. 

Die Nutzer:innen interagieren über eine Weboberfläche, während die Administration über eine Backend-Komponente erfolgt.

Folgende externe Akteure und Systeme interagieren mit Studurizer:

| Externe Instanz           | Beschreibung                                                             |
|---------------------------|--------------------------------------------------------------------------|
| **Studierende**           | Erhalten Kurseinblicke, laden Materialien herunter, reichen Aufgaben ein |
| **Dozierende**            | Verwalten Kurse, laden Inhalte hoch, verwalten Teilnahmen                |
| **Administrator:innen**   | Erstellen Benutzerkonten, richten Kurse ein, konfigurieren das System    |
| **Barrierefreiheitsbeauftragte** | Prüfen die Umsetzung von WCAG 2.2-Standards                              |
| **Datenschutzbeauftragte:r** | Kontrolliert Einhaltung von DSGVO-Vorgaben                               |
| **Hochschulverwaltung**   | Beobachtet Kursbetrieb, ggf. für Reporting relevant                      |
| **Externe KI-Dienste**    | Optional: z. B. automatische Textzusammenfassungen oder Voice-Interface  |
| **Mailserver**            | Versendet Zertifikate                                                    |

---

## Technischer Kontext (Diagramm)

```mermaid
graph TD
    A[Studierende] -->|Web-UI| S[Studurizer]
    B[Dozierende] -->|Web-UI| S
    C[Administrator:innen] -->|Admin-Panel| S
    D[Barrierefreiheitsbeauftragte] -->|Feedback/Review| S
    E[Datenschutzbeauftragte:r] -->|Audits| S
    F[Hochschulverwaltung] -->|Berichte| S
    S -->|Interne REST Abfragen | K[ KI Dienst API ]
    S -->|E-Mail templating | H[Mailserver]
    H -->|E-Mail Zertifikatuebermittlung| A
