# Datenbankmodul und Datenbank laden
import sqlite3
datenbank = sqlite3.connect("Lektorat.db")
cur = datenbank.cursor()
with open("init-db.sql") as initfile:
    initfile = initfile.read()
    datenbank.executescript(initfile)

#Bibliothek zur Zeitberechnung
import datetime

#diverse Bibliothekem
from tabulate import tabulate, SEPARATING_LINE # Um Tabellen in der Kommandozeile ausgeben zu können
import re  # Für Regular Expressions
import os
from os import system, name

#Definition der Menüs
menu_ = (
    ("1", "Zeiten"),
    ("2", "Projekte"),
    ("3", "Kunden"),
    ("4", "Rechnungen"),
    ("5", "Programm beenden")
)

# Definition von Ja/Nein-Variablen für Ja/Nein-Abfragen
janein = ["j", "ja", "J", "Ja", "n", "nein", "N", "Nein", "y", "Y", "yes", "Yes", "No", "no"]
ja = ["j", "ja", "J", "Ja", "y", "Y", "yes", "Yes"]
nein = ["n", "nein", "N", "Nein", "No", "no"]

def clear(): # Clearscreen-Funktion
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')
def menu():
    clear()
    eingabepruf = []
    [eingabepruf.append(item[0]) for item in menu_]
    print(tabulate(menu_, headers = ["ID", "Beschreibung"], tablefmt="rounded_outline"))
    eingabe = ""
    while eingabe not in eingabepruf:
        eingabe = input("Auswahl: ")
        if eingabe not in eingabepruf:
            print("Sorry, es existiert kein Modul mit dieser ID!")
    if eingabe == "1":
        zeitenmenu()
    elif eingabe == "2":
        projektemenu()
    elif eingabe == "3":
        kundenmenu()
    elif eingabe == "4":
        rechnungenmenu()
    elif eingabe == "5":
        datenbank.close()
        clear()
        return()

def zeitenmenu():
    clear()
    menu_zeiten = (
        ("1", "Zeiten eintragen"),
        ("2", "Noch nicht abgerechnete Zeiten anzeigen"),
        ("3", "Zurück zum Hauptmenü")
    )
    eingabepruf = []
    [eingabepruf.append(item[0]) for item in menu_zeiten]
    print(tabulate(menu_zeiten, headers=["ID", "Beschreibung"], tablefmt="rounded_outline"))
    eingabe = ""
    while eingabe not in eingabepruf:
        eingabe = input("Auswahl: ")
        if eingabe not in eingabepruf:
            print("Sorry, es existiert kein Modul mit dieser ID!")
    if eingabe == "1":
        eintrag_zeit()
    elif eingabe == "2":
        anzeige_zeiten()
    elif eingabe == "3":
        menu()
        return()

def projektemenu():
    clear()
    menu_projekte = (
        ("1", "Laufende Projekte anzeigen"),
        ("2", "Ein neues Projekt eintragen"),
        ("3", "Ein Projekt abschließen"),
        ("4", "Zurück zum Hauptmenü")
    )
    eingabepruf = []
    [eingabepruf.append(item[0]) for item in menu_projekte]
    print(tabulate(menu_projekte, headers=["ID", "Beschreibung"], tablefmt="rounded_outline"))
    eingabe = ""
    while eingabe not in eingabepruf:
        eingabe = input("Auswahl: ")
        if eingabe not in eingabepruf:
            print("Sorry, es existiert kein Modul mit dieser ID!")
    if eingabe == "1":
        anzeige_projekte()
    elif eingabe == "2":
        eintrag_projekt()
    elif eingabe == "3":
        projekt_abschluss()
    elif eingabe == "4":
        menu()
        return()

def kundenmenu():
    clear()
    menu_kunden = (
        ("1", "Kunden anzeigen"),
        ("2", "Einen neuen Kunden anlegen"),
        ("3", "Zurück zum Hauptmenü")
    )
    eingabepruf = []
    [eingabepruf.append(item[0]) for item in menu_kunden]
    print(tabulate(menu_kunden, headers=["ID", "Beschreibung"], tablefmt="rounded_outline"))
    eingabe = ""
    while eingabe not in eingabepruf:
        eingabe = input("Auswahl: ")
        if eingabe not in eingabepruf:
            print("Sorry, es existiert kein Modul mit dieser ID!")
    if eingabe == "1":
        clear()
        cur.execute("SELECT * FROM Kunden")
        kunden = cur.fetchall()
        kunden.append(SEPARATING_LINE)
        print(tabulate(kunden, headers = ["Name Zeile 1", "Name Zeile 2", "Name Zeile 3", "Straße", "Ort"]))
        input("Bitte Enter drücken, um zum Kundenmenü zurückzukehren.")
        kundenmenu()
    elif eingabe == "2":
        eintrag_kunde(0)
    elif eingabe == "3":
        menu()
        return()

def rechnungenmenu():
    clear()
    menu_rechnungen = (
        ("1", "Noch nicht abgerechnete Zeiten anzeigen"),
        ("2", "Unbezahlte Rechnungen anzeigen"),
        ("3", "Eine Rechnung erstellen"),
        ("4", "Alle Rechnungen anzeigen"),
        ("5", "Rechnung als bezahlt markieren"),
        ("6", "Zurück zum Hauptmenü")
    )
    eingabepruf = []
    [eingabepruf.append(item[0]) for item in menu_rechnungen]
    print(tabulate(menu_rechnungen, headers=["ID", "Beschreibung"], tablefmt="rounded_outline"))
    eingabe = ""
    while eingabe not in eingabepruf:
        eingabe = input("Auswahl: ")
        if eingabe not in eingabepruf:
            print("Sorry, es existiert kein Modul mit dieser ID!")
    if eingabe == "1":
        anzeige_zeiten()
    elif eingabe == "2":
        anzeige_rechnungen_unbezahlt()
    elif eingabe == "3":
        rechnung_erstellen()
    elif eingabe == "4":
        anzeige_rechnungen_alle()
    elif eingabe == "5":
        rechnung_bezahlt()
    elif eingabe == "6":
        menu()
        return()
def eintrag_zeit():
    clear()
    cur.execute("SELECT rowid, Name, Kunde FROM Projekte WHERE Abgeschlossen = 0")
    projektliste_sql = cur.fetchall()
    #print(projektliste_sql)
    projektliste = []
    pruefung_projekte = []
    for item in projektliste_sql:
        projektid = item[0]
        projektname = item[1]
        cur.execute("SELECT NameZeile1 FROM Kunden WHERE rowid = ?", str(item[2]))
        kundenname = cur.fetchall()[0][0]
        pruefung_projekte.append(str(projektid))
        projektliste.append([projektid, projektname, kundenname])
    print(tabulate(projektliste, headers = ["Projekt-ID", "Titel", "Kunde"]))
    projekt = ""
    while projekt not in pruefung_projekte:
        projekt = input("Für welches Projekt hast du gearbeitet? Bitte die ID eingeben: ")
        if projekt not in pruefung_projekte:
                print("Sorry, das Projekt ist nicht in der Liste!")
    anfangszeit = ""
    while re.fullmatch("\d\d\:\d\d", anfangszeit) == None:
        anfangszeit = input("Wann hast du angefangen? ")
        if re.fullmatch("\d\d\:\d\d", anfangszeit) == None:
            print("Bitte eine gültige Uhrzeit eingeben!")
    endzeit = ""
    while re.fullmatch("\d\d\:\d\d", endzeit) == None:
        endzeit = input("Wann hast du aufgehört? ")
        if re.fullmatch("\d\d\:\d\d", endzeit) == None:
            print("Bitte eine gültige Uhrzeit eingeben!")
    zeit = datetime.datetime.strptime(endzeit, "%H:%M") - datetime.datetime.strptime(anfangszeit, "%H:%M")
    datum = datetime.date.today()
    datum = datum.strftime("%d.%m.%Y")
    cur.execute("INSERT INTO Zeiten VALUES(?, ?, ?, ?, ?, '0', NULL)", (datum, anfangszeit, endzeit, str(zeit), projekt))
    datenbank.commit()
    menu()


def eintrag_projekt():
    clear()
    cur.execute("SELECT rowid, Name, Kunde FROM Projekte WHERE Abgeschlossen = 0")
    projektliste_sql = cur.fetchall()
    # print(projektliste_sql)
    projektliste = []
    pruefung_projekte = []
    for item in projektliste_sql:
        projektid = item[0]
        projektname = item[1]
        cur.execute("SELECT NameZeile1 FROM Kunden WHERE rowid = ?", str(item[2]))
        kundenname = cur.fetchall()[0][0]
        pruefung_projekte.append(str(projektid))
        projektliste.append([projektid, projektname, kundenname])
    projektliste.append(SEPARATING_LINE)
    print("Aktuelle Projekte:")
    print(tabulate(projektliste, headers=["Projekt-ID", "Titel", "Kunde"]))
    projektvorhanden = ""
    while projektvorhanden not in janein:
        projektvorhanden = input("Ist das Projekt schon vorhanden (j/n)? ")
        if projektvorhanden not in janein:
            print("Uneindeutige Antwort. Bitte j oder n eingeben!")
    if projektvorhanden in ja:
        print("Das Projekt ist schon in der Datenbank vorhanden, es muss nicht mehr eingetragen werden.")
        input("Bitte Enter drücken, um zum Hauptbildschirm zurückzukehren.")
        menu()
        return()
    titel = input("Bitte den Titel des Projekts eingeben: ")
    cur.execute("SELECT rowid, NameZeile1 FROM Kunden")
    kundenliste = cur.fetchall()
    kundenliste.append(SEPARATING_LINE)
    kundenidprufung = ["0"]
    [kundenidprufung.append(str(item[0])) for item in kundenliste]
    print(kundenidprufung)
    print("\n", tabulate(kundenliste, headers = ["ID", "Kunde"]))
    kunde = ""
    while kunde not in kundenidprufung:
        kunde = input("Bitte die ID des Kunden eingeben. Wenn der Kunde noch nicht vorhanden ist, bitte die 0 eingeben: ")
        [print("Sorry, die eingegebene ID entspricht keinem Kunden! Bitte erst den Kunden anlegen.") if kunde not in kundenidprufung else None]
        if kunde == "0":
            eintrag_kunde(1)
            return
    anmerkungen = input("Gibt es weitere Informationen (z.B. Bestellnummer) zum Projekt? Bitte eingeben: ")
    cur.execute("INSERT INTO Projekte VALUES(?, ?, 0, ?)", (titel, kunde, anmerkungen))
    datenbank.commit()
    menu()

def eintrag_kunde(referrer):
    '''
    Die referrer-Variable kommt zum Einsatz, wenn die Funktion von einer anderen Funktion aus aufgerufen wurde,
    weil z.B. für einen Projekteintrag der Kunde noch nicht in der Datenbank existiert.
    Der Schlüssel ist wie folgt:
    Wert 0 für einen Aufruf aus dem Hauptmenü
    Wert 1 für einen Aufruf aus der eintrag_projekt-Funktion
    '''
    clear()
    cur.execute("SELECT NameZeile1 FROM Kunden")
    kundenliste = cur.fetchall()
    print("Bisher eingetragene Kunden:\n", tabulate(kundenliste))
    namezeile1 = input("Bitte die erste Zeile der Anschrift des neuen Kunden eingeben: ")
    weiter = ""
    while weiter not in janein:
        weiter = input("Gibt es weitere Namenszeilen (j/n)? ")
        [print("Bitte entweder j oder n eingeben!") if weiter not in janein else None]
    if weiter in ja:
        namezeile2 = input("Bitte die zweite Zeile der Anschrift des neuen Kunden eingeben: ")
        namezeile3 = input("Bitte die dritte Zeile der Anschrift des neuen Kunden eingeben: ")
    strasse = input("Bitte die Straße und Hausnummer eingeben: ")
    ort = input("Bitte PLZ und Ort eingeben: ")
    if weiter in ja:
        cur.execute("INSERT INTO Kunden VALUES(?, ?, ?, ?, ?)", (namezeile1, namezeile2, namezeile3, strasse, ort))
    else:
        cur.execute("INSERT INTO Kunden VALUES(?, NULL, NULL, ?, ?)", (namezeile1, strasse, ort))
    datenbank.commit()
    if referrer == 1:
        clear()
        eintrag_projekt()
    else:
        menu()

def rechnung_erstellen():
    mehrere = ""
    zeitenliste = []
    projektausgewaehlt = ["0"]
    projekte = []
    while mehrere not in nein:
        mehrere = ""
        clear()
        cur.execute("SELECT rowid, Name FROM Projekte WHERE Abgeschlossen = 0 AND rowid NOT IN ({0})".format(', '.join('?' for _ in projektausgewaehlt)), projektausgewaehlt)
        projektliste = cur.fetchall()
        projektliste.append(SEPARATING_LINE)
        print(tabulate(projektliste, headers = ["ID", "Titel"]))
        projektauswahl = input("Welches Projekt soll abgerechnet werden? Bitte ID eingeben: ")
        projektausgewaehlt.append(projektauswahl)
        cur.execute("SELECT rowid, Name, Kunde FROM Projekte WHERE rowid = ?", (projektauswahl))
        projekt = cur.fetchone()
        projekt = list(projekt)
        if len(projektausgewaehlt) > 2:
            if projekte[0][2] != projekt[2]:
                print("Dieses Projekt ist einem anderen Kunden zugeordnet und kann daher nicht in derselben Rechnung wie das zuvor ausgewählte Projekt abgerechnet werden.")
                auswahl = (("1", "Ein anderes Projekt zur Rechnung hinzufügen"), ("2", "Mit der Rechnungserstellung fortfahren"), SEPARATING_LINE)
                print(tabulate(auswahl, headers=["ID","Aktion"]))
                eingabe = ""
                while eingabe not in ("1", "2"):
                    eingabe = input("Wie soll fortgefahren werden? ")
                    if eingabe not in ("1", "2"):
                        print("Bitte einen gültigen Wert eingeben.")
                if eingabe == "1":
                    mehrere = "j"
                    continue
                elif eingabe == "2":
                    mehrere = "n"
                    continue
        projekt[0] = str(projekt[0])
        projekt[1] = input("Bitte die Beschreibung der Leistung eingeben: ") + f" {projekt[1]}"
        stundensatz = input("Bitte den für diese Leistung anzulegenden Stundensatz in Euro eingeben: ")
        projekt.append(stundensatz)
        cur.execute("SELECT Datum, Zeit, Projekt FROM Zeiten WHERE Abgerechnet = 0 AND Projekt = ?", (projekt[0]))
        zeiten = cur.fetchall()
        zeiten = list(zeiten)
        for item in zeiten:
            zeitenliste.append(item)
        if zeiten == []:
            print("Für dieses Projekt gibt es keine noch nicht abgerechneten Zeiten!")
            input("Bitte Enter drücken, um zum Rechnungsmenü zurückzukehren.")
            rechnungenmenu()
            return()
        projekte.append(projekt)
        if len(projektliste) > 2:
            while mehrere not in janein:
                    mehrere = input("Sollen weitere Projekte in der Rechnung abgerechnet werden (j/n)? ")
                    if mehrere not in janein:
                        print("Ungültige Eingabe. Bitte j oder n eingeben!")
        else:
            mehrere = "n"
    cur.execute("SELECT rowid, NameZeile1, NameZeile2, NameZeile3, Straße, Ort FROM Kunden WHERE rowid = ?", (str(projekte[0][2])))
    kunde = list(cur.fetchone())
    kunde.remove(None)
    anschrift = ""
    kundennummer = kunde[0]
    index = 0
    for item in kunde:
        if index > 0:
            anschrift = anschrift + item + "\\\\"
        index = index + 1
    anschrift = anschrift.rstrip(anschrift[-1])
    anschrift = anschrift.replace("&", "\&")
    for projekt in projekte:
        cur.execute("UPDATE Zeiten SET Abgerechnet = 1 WHERE Abgerechnet = 0 AND Projekt = ?", (projekt[0]))
    tabellenzeilen = []
    position = 1
    gesamt = 0
    gesamtstunden = datetime.timedelta(hours = 0, minutes = 0)
    for projekt in projekte:
        for zeiten in zeitenliste:
            if zeiten[2] == int(projekt[0]):
                stunden = zeiten[1].split(":")
                stunden = datetime.timedelta(hours=int(stunden[0]), minutes=int(stunden[1]))
                gesamtstunden = gesamtstunden + stunden
                stunden = stunden.total_seconds() / 3600
                stundensatz = int(projekt[3])
                betrag = stunden * stundensatz
                betrag = round(betrag, 2)
                gesamt = gesamt + betrag
                gesamt = round(gesamt, 2)
                betrag = str(betrag)
                betrag = betrag.replace(".", ",")
                while len(betrag) < 5:
                    betrag = betrag + "0"
                tabellenzeilen.append([str(position), zeiten[0], projekt[1], zeiten[1], projekt[3], betrag])
                position = position + 1
    gesamt = str(gesamt)
    gesamt = gesamt.replace(".", ",")
    while len(gesamt) < 5:
        gesamt = gesamt + "0"
    gesamtstunden = str(gesamtstunden).split(":")
    gesamtstunden = f"{gesamtstunden[0]}:{gesamtstunden[1]}"
    if len(gesamtstunden) < 5:
        gesamtstunden = "0" + gesamtstunden
    tabellenzeilen.append("LINIE")
    tabellenzeilen.append(["Gesamtbetrag", gesamtstunden, gesamt])
    tabelle = ""
    for zeile in tabellenzeilen:
        if zeile != "LINIE" and zeile[0] != "Gesamtbetrag":
            tabelle = f"{tabelle} {zeile[0]} & {zeile[1]} & {zeile[2]} & {zeile[3]} & {zeile[4]} € & {zeile[5]} € \\\\"
        elif zeile == "LINIE":
            tabelle = f"{tabelle} \\midrule "
        elif zeile[0] == "Gesamtbetrag":
            tabelle = tabelle + "\\multicolumn{3}{l}{\\textbf{" + zeile[0] + "}} & \\textbf{" + zeile[1] + "} &  & \\textbf{" + zeile[2] + " €}"
    cur.execute("SELECT MAX(rowid) FROM Rechnungen")
    lrid = cur.fetchone()
    rechnungsnummer = lrid[0] + 1
    rechnungsnummer = f"{rechnungsnummer:03}"
    for projekt in projekte:
        cur.execute("UPDATE Zeiten SET Rechnungsnummer = ? WHERE Abgerechnet = 0 AND Projekt = ?", (rechnungsnummer, projekt[0]))
        cur.execute("UPDATE Zeiten SET Abgerechnet = 1 WHERE Abgerechnet = 0 AND Projekt = ?", (projekt[0]))
    dateiname = f"Rechnung-{rechnungsnummer}"
    with open("Vorlage_Rechnung.tex") as file:
        vorlage = file.read()
    vorlage = vorlage.replace("\\VAR{ADRESSE}", anschrift)
    vorlage = vorlage.replace("\\VAR{RECHNUNGSNUMMER}", rechnungsnummer)
    vorlage = vorlage.replace("\\VAR{TABELLE}", tabelle)
    with open(f"./Rechnungen/{dateiname}.tex", "x") as file:
        file.write(vorlage)
    os.system(f'pdflatex --interaction=batchmode -output-directory ./Rechnungen {dateiname}.tex 2>&1 > /dev/null')
    os.remove(f"./Rechnungen/{dateiname}.aux")
    os.remove(f"./Rechnungen/{dateiname}.log")
    os.rename(f"./Rechnungen/{dateiname}.tex", f"./Rechnungen/Texfiles/{dateiname}.tex")
    datum = datetime.date.today()
    datum = datum.strftime("%d.%m.%Y")
    cur.execute("INSERT INTO Rechnungen VALUES(?, ?, ?, 0, NULL, ?)", (rechnungsnummer, gesamt, datum, kundennummer))
    datenbank.commit()
    menu()

def projekt_abschluss():
    cur.execute("SELECT rowid, Name FROM Projekte WHERE Abgeschlossen = 0")
    projektliste = cur.fetchall()
    projektliste = list(projektliste)
    projektliste.append(SEPARATING_LINE)
    print(tabulate(projektliste, headers=["ID", "Titel"]))
    projektauswahl = input("Welches Projekt wurde abgeschlossen? Bitte ID eingeben: ")
    cur.execute("UPDATE Projekte SET Abgeschlossen = 1 WHERE rowid = ?", (projektauswahl))
    datenbank.commit()
    menu()

def anzeige_zeiten():
    clear()
    cur.execute("SELECT Datum, Anfang, Ende, Zeit, Projekt FROM Zeiten WHERE Abgerechnet = 0")
    zeiten = cur.fetchall()
    if zeiten == []:
        print("Es gibt keine noch nicht abgerechneten Zeiten.")
    else:
        print(tabulate(zeiten, headers = ["Datum", "Anfang", "Ende", "Zeit", "Projekt"]))
    input("Bitte Enter drücken, um zum Zeiten-Menu zurückzukehren.")
    zeitenmenu()
    return ()

def anzeige_projekte():
    clear()
    cur.execute("SELECT Name, Kunde, Anmerkungen FROM Projekte WHERE Abgeschlossen = 0")
    projekte = cur.fetchall()
    projektliste = []
    for item in projekte:
        kundenid = str(item[1])
        cur.execute("SELECT NameZeile1 FROM Kunden WHERE rowid = ?", kundenid)
        kunde = cur.fetchone()
        kunde = str(kunde[0])
        projektliste.append((item[0], kunde, item[2]))
    print(tabulate(projektliste, headers = ["Titel", "Kunde", "Anmerkungen"]))
    input("Bitte Enter drücken, um zum Projekte-Menu zurückzukehren.")
    projektemenu()
    return()

def anzeige_rechnungen_unbezahlt():
    clear()
    cur.execute("SELECT Rechnungsnummer, Rechnungshöhe, Rechnungsdatum, Kunde FROM Rechnungen WHERE Gezahlt = 0")
    rechnungen = cur.fetchall()
    if rechnungen == []:
        print("Es gibt keine offenen Rechnungen.")
        input("Bitte Enter drücken, um zum Rechnungsmenü zurückzukehren.")
        rechnungenmenu()
        return()
    else:
        rechnungsliste = []
        for item in rechnungen:
            kundenid = str(item[3])
            cur.execute("SELECT NameZeile1 FROM Kunden WHERE rowid = ?", kundenid)
            kunde = cur.fetchone()
            kunde = str(kunde[0])
            rechnungsliste.append((item[0], kunde, item[1], item[2]))
        rechnungsliste.append(SEPARATING_LINE)
        print(tabulate(rechnungsliste, headers = ["Rechnungsnummer", "Kunde", "Höhe", "Datum"]))
        input("Bitte Enter drücken, um zum Rechnungsmenü zurückzukehren.")
        rechnungenmenu()
        return(rechnungen)

def anzeige_rechnungen_alle():
    clear()
    cur.execute("SELECT Rechnungsnummer, Rechnungshöhe, Rechnungsdatum, Gezahlt, Zahlungseingang, Kunde FROM Rechnungen")
    rechnungen = cur.fetchall()
    rechnungsliste = []
    for item in rechnungen:
        kundenid = str(item[5])
        cur.execute("SELECT NameZeile1 FROM Kunden WHERE rowid = ?", kundenid)
        kunde = cur.fetchone()
        kunde = str(kunde[0])
        if item[3] == 1:
            gezahlt = "Gezahlt"
        else:
            gezahlt = "Ungezahlt"
        rechnungsliste.append((item[0], kunde, item[1], item[2], gezahlt, item[4]))
    rechnungsliste.append(SEPARATING_LINE)
    print(tabulate(rechnungsliste, headers = ["Rechnungsnummer", "Kunde", "Höhe", "Rechnungsdatum", "Status", "Datum Zahlungseingang"]))
    input("Bitte Enter drücken, um zum Rechnungsmenü zurückzukehren.")
    rechnungenmenu()
    return()

def rechnung_bezahlt():
    clear()
    cur.execute("SELECT Rechnungsnummer, Rechnungshöhe, Rechnungsdatum, Kunde FROM Rechnungen WHERE Gezahlt = 0")
    rechnungen_data = cur.fetchall()
    if rechnungen_data == []:
        print("Es gibt keine offenen Rechnungen.")
        input("Bitte Enter drücken, um zum Rechnungsmenü zurückzukehren.")
        rechnungenmenu()
        return()
    rechnungsliste = []
    for item in rechnungen_data:
        kundenid = str(item[3])
        cur.execute("SELECT NameZeile1 FROM Kunden WHERE rowid = ?", kundenid)
        kunde = cur.fetchone()
        kunde = str(kunde[0])
        rechnungsliste.append((item[0], kunde, item[1], item[2]))
    rechnungsliste.append(SEPARATING_LINE)
    print(tabulate(rechnungsliste, headers=["Rechnungsnummer", "Kunde", "Höhe", "Datum"]))
    rechnungsliste = []
    for rechnung in rechnungen_data:
        rechnungsliste.append(rechnung[0])
    rechnungsnummer = "99999999"
    # print(rechnungen_liste)
    rechnungsnummer = input("Welche Rechnung wurde gezahlt? Bitte Rechnungsnummer eingeben: ")
    while rechnungsnummer not in rechnungsliste:
        print(f"Die eingegebene Rechnungsnummer ({rechnungsnummer}) existiert nicht!")
        rechnungsnummer = input("Bitte Rechnungsnummer eingeben: ")
    cur.execute("UPDATE Rechnungen SET Gezahlt = 1 WHERE Rechnungsnummer = ?", (rechnungsnummer,))
    datum = input("Bitte das Datum des Zahlungseingangs eingeben (Format TT.MM.JJJJ): ")
    cur.execute("UPDATE Rechnungen SET Zahlungseingang = ? WHERE Rechnungsnummer = ?", (datum, rechnungsnummer))
    input("Bitte Enter drücken, um zum Projekte-Menu zurückzukehren.")
    datenbank.commit()
    rechnungenmenu()


menu()