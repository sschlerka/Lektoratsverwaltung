# Lektoratsverwaltung
Es handelt sich hierbei um ein kleines Hilfsprogramm, das mir die Verwaltung meiner Tätigkeit als Lektor, Korrektor und Textsetzer erleichert.

Das Programm läuft über ein Kommandozeileninterface, das mit Hilfe von tabulate erstellt wurde. Die Daten werden in einer SQLite-Datenbank gespeichert.

## Voraussetzungen
Folgende Python-Bibliotheken werden vorausgesetzt: sqlite3, datetime, tabulate, re, os
  
Zudem ist für die automatische Rechnungserstellung eine LaTeX-Distribution nötig, da hier das pdftex-Kommando aufgerufen wird. Getestet wurde die Funktion mit TeXLive unter Linux.

In der Datei Vorlage_Rechnung.tex müssen vor Benutzung Platzhalter für Name, Anschrift, Telefonnummer, Mailadresse und Bankverbindung ausgetauscht werden. Außerdem muss die Datei signature.pdf durch eine digitalisierte Unterschrift ersetzt werden.

## Funktionen
- Arbeitszeiten:
  - Eintragen von Arbeitszeiten
  - Anzeige noch nicht abgerechneter Arbeitszeiten
- Projekte:
  - Anzeige laufender Projekte
  - Eintragen neuer Projekte in die Datenbank
  - Projektstatus auf "abgeschlossen" ändern
- Kunden:
  - Anzeige von Kundendaten
  - Anlegen neuer Kundendaten
- Rechnungen:
  - Anzeige von Rechnungen (unbezahlte Rechnungen und alle bislang gestellten Rechnungen)
  - Automatische Rechnungserstellung mittels einer LaTeX-Vorlage
  - Rechnungsstatus auf "bezahlt" ändern


