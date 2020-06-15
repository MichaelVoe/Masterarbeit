import random
from pathlib import Path
from solve_pddl import get_cost

data_folder = Path("/home/familie/symk/domains/")

sample_pddl_pfad = data_folder / "Sample.pddl"

ziel_pddl_pfad = ["ziel_pfad"] * 5
ziel_pddl_pfad[0] = data_folder /"Ziel0.pddl"
ziel_pddl_pfad[1] = data_folder /"Ziel1.pddl"
ziel_pddl_pfad[2] = data_folder /"Ziel2.pddl"
ziel_pddl_pfad[3] = data_folder /"Ziel3.pddl"
ziel_pddl_pfad[4] = data_folder /"Ziel4.pddl"


zufaelliges_lab = 1  # zufälliges lab ein/aus schalten 1=an

anzahl_felder = 49  # 7x7 Feld
anzahl_gesperrte_felder = 10
feld = [0] * anzahl_felder

def make_lab():
    for i in range(
            anzahl_felder):  # Feld[] wird mit nullen entsprechend der Anzahl gesperrten felder gefüllt, rest mit einsen
        if (i < anzahl_gesperrte_felder):
            feld[i] = 0
        else:
            feld[i] = 1
    random.shuffle(feld)  # Feld[] wird zufällig gemischt

    x = y = m = n = 0
    dreiodervier = einsoderzwei = 10

    while (True):
        wrong = 0
        for i in range(1, 5):
            u = p = o = 0
            sample_pddl = open(sample_pddl_pfad, 'r')
            new_pddl = open(ziel_pddl_pfad[i], 'w+')
            for textzeile in sample_pddl:
                # Alle Zeilen die entscheiden ob gesperrt oder nicht und nicht der Initialzustand 3-3 (soll offen bleiben)
                if ((textzeile.find('open') != -1) or (textzeile.find('locked') != -1)) and (zufaelliges_lab == 1):
                    if (feld[o] == 0 and o != 24):  # 24 ist Startfeld vom Spielstein und soll immer offen sein
                        textzeile = "          (locked node" + str(p) + "-" + str(u) + ")" + '\n'
                    else:
                        textzeile = "          (open node" + str(p) + "-" + str(u) + ")" + '\n'
                    new_pddl.write(textzeile)
                    o = o + 1
                    u = u + 1
                    if (u == 7):
                        u = 0
                        p = p + 1
                elif (textzeile.find('goal') != -1):  # Ziele werden zufällig geändert (1-gemeinsames Ziel und 2 unterschiedliche Ziele)
                    while (True):
                        x = random.randrange(7)  # int Zufallszahl zwischen 0-6 (ganzzahlig)
                        y = random.randrange(7)
                        if (x != 3 and y != 3):
                            break
                    if (m == 0):
                        dreiodervier = random.randrange(3,5)# Ziel3 oder Ziel4 werden gleich dem gemeinsamen bereits vergeben Ziel1 oder Ziel2
                        m = 1
                    if (i == dreiodervier):
                        x = x_gemeinsam
                        y = y_gemeinsam
                    textzeile = "   (:goal (and (at-robot node" + str(x) + "-" + str(y) + "))))" + '\n'
                    new_pddl.write(textzeile)
                    if (n == 0):
                        einsoderzwei = random.randrange(1,3)
                        n = 1
                    if (i == einsoderzwei):
                        x_gemeinsam = x
                        y_gemeinsam = y
                else:
                    new_pddl.write(textzeile)

            new_pddl.close()
            sample_pddl.close()

        # Check ob alle Ziele frei begehbar sind
        ziel_ausgabe = ["0"] * 5
        if(wrong != 1):
            for i in range(1, 5):
                test_pddl = open(ziel_pddl_pfad[i], 'r')
                for textzeile in test_pddl:
                    if (textzeile.find('goal') != -1):
                        ziel = textzeile[29:32]
                        ziel_ausgabe[i] = ziel
                test_pddl.close()
                test_pddl = open(ziel_pddl_pfad[i], 'r')
                for textzeile in test_pddl:
                    if ((textzeile.find('locked') != -1) and (textzeile.find(ziel) != -1)):
                        #print(textzeile)
                        #print("file ist fehlerhaft")
                        wrong = 1
                test_pddl.close()

        # Check ob die beiden nicht gemeinsamen Ziele nicht zufällig gleich dem gemeinsamen Ziel sind
        if(wrong != 1):
            uebereinstimmung = 0
            for i in range(1,5):
                for n in range(1,5):
                    if(ziel_ausgabe[i] == ziel_ausgabe[n]):
                        uebereinstimmung = uebereinstimmung + 1

            if(uebereinstimmung >= 7):
                wrong = 1

        # Check ob es Weg zu den Zielen gibt und sie nicht "zugebaut" sind
        if(wrong != 1):
            for i in range(1,5):
                cost = get_cost(i)
                if(cost == 0):
                    wrong = 1

        if (wrong != 1):
            break

    for i in range(1,5):
        print(ziel_ausgabe[i])

    return feld, ziel_ausgabe[1], ziel_ausgabe[2], ziel_ausgabe[3],ziel_ausgabe[4]