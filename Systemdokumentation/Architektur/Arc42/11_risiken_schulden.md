# 11 – Risiken und technische Schulden

In diesem Kapitel werden bekannte Projektrisiken sowie technische Schulden dokumentiert, die bewusst (z. B. aus Zeit- oder Aufwandsgründen) in Kauf genommen wurden. Diese Punkte sollten im späteren Projektverlauf priorisiert beobachtet und ggf. behoben werden.

---

## Technische Schulden

### 1. Kein Einsatz eines modernen Frontend-Frameworks (z. B. Angular, React, Vue)

**Auswirkung:**  
Die Benutzeroberfläche basiert vollständig auf **klassischem serverseitigem Templating** mit Django.  
Dies vereinfacht die Entwicklung und verbessert die Barrierefreiheit, limitiert jedoch das Potenzial für moderne, dynamische UI-Interaktionen.

**Begründung:**  
- Einfachere Wartung
- Bessere Einsteigerfreundlichkeit
- Barrierefreiheit lässt sich serverseitig einfacher kontrollieren

**Risiko:**  
- Die UI wirkt weniger „modern“ oder responsiv im Vergleich zu Single-Page-Anwendungen
- Erweiterungen (z. B. Live-Chat, Drag&Drop, Vorschau etc.) sind deutlich schwerer umzusetzen

---

### 2. Verwendung von SQLite statt PostgreSQL

**Auswirkung:**  
Das System speichert alle Daten in einer lokalen, dateibasierten SQLite-Datenbank. Diese ist für Prototypen und kleine Installationen geeignet, aber nicht für den produktiven Mehrbenutzerbetrieb mit parallelen Zugriffen.

**Begründung:**  
- Kein Setup notwendig
- Ideal für initiale Entwicklung
- ORM-kompatibel für spätere Migration

**Risiko:**  
- Performanceprobleme bei hoher Nutzeranzahl
- Umstellung auf PostgreSQL notwendig, inkl. Anpassung an Produktionsumgebung, Migrationsskripte etc.

---

## Weitere potenzielle Risiken

| Risiko | Beschreibung | Mögliche Gegenmaßnahme |
|--------|--------------|-------------------------|
| Ressourcenknappheit | Kleines studentisches Team mit begrenzter Zeit | Priorisierung der Kernfunktionen, technische Schulden bewusst dokumentieren |
| Barrierefreiheit unterschätzt | Umsetzung von WCAG 2.2 ist komplexer als zunächst gedacht | Feedback von Testgruppen, frühe Tests mit Screenreadern |
| Datenschutzanforderungen steigen | Neue DSGVO-Interpretationen oder Anforderungen durch Hochschulen | Enge Abstimmung mit Datenschutzbeauftragten, Vorbereitung auf Erweiterungen |
