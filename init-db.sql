
CREATE TABLE IF NOT EXISTS "Kunden" (
	"NameZeile1"	TEXT,
	"NameZeile2"	TEXT,
	"NameZeile3"	TEXT,
	"Straße"	TEXT,
	"Ort"	TEXT
);
CREATE TABLE IF NOT EXISTS "Projekte" (
	"Name"	TEXT,
	"Kunde"	INTEGER NOT NULL,
	"Abgeschlossen"	INTEGER NOT NULL DEFAULT 0,
	"Anmerkungen"	TEXT
);
CREATE TABLE IF NOT EXISTS "Rechnungen" (
	"Rechnungsnummer"	TEXT,
	"Rechnungshöhe"	TEXT,
	"Rechnungsdatum"	TEXT,
	"Gezahlt"	INTEGER DEFAULT 0,
	"Zahlungseingang"	TEXT,
	"Kunde"	INTEGER
);
CREATE TABLE IF NOT EXISTS "Zeiten" (
	"Datum"	TEXT NOT NULL,
	"Anfang"	TEXT NOT NULL,
	"Ende"	TEXT NOT NULL,
	"Zeit"	TEXT NOT NULL,
	"Projekt"	INTEGER,
	"Abgerechnet"	INTEGER DEFAULT 0,
	"Rechnungsnummer"	TEXT
)
