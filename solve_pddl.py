import os
from pathlib import Path

data_folder = Path("/home/familie/symk/domains/")
plan_folder = Path("/home/familie/symk/repo/Pathplaning/found_plans")

ziel_pddl_pfad = ["Zielpfad"]*5
ziel_pddl_pfad[1] = data_folder / "Ziel1.pddl"
ziel_pddl_pfad[2] = data_folder / "Ziel2.pddl"
ziel_pddl_pfad[3] = data_folder / "Ziel3.pddl"
ziel_pddl_pfad[4] = data_folder / "Ziel4.pddl"

neuer_ziel_pddl_pfad = ["Zielpfad"]*5
neuer_ziel_pddl_pfad[1] = data_folder / "Ziel1_new.pddl"
neuer_ziel_pddl_pfad[2] = data_folder / "Ziel2_new.pddl"
neuer_ziel_pddl_pfad[3] = data_folder / "Ziel3_new.pddl"
neuer_ziel_pddl_pfad[4] = data_folder / "Ziel4_new.pddl"

z1_anzahl_erster_schritt = z2_anzahl_erster_schritt = z3_anzahl_erster_schritt = z4_anzahl_erster_schritt = []
z1_set_erste_schritte = z2_set_erste_schritte = z3_set_erste_schritte = z4_set_erste_schritte = []
z1_gesamtanzahl_erste_schritte = z2_gesamtanzahl_erste_schritte = z3_gesamtanzahl_erste_schritte = z4_gesamtanzahl_erste_schritte = []

p_Z1_old = p_Z2_old = p_Z3_old = p_Z4_old = 0.5

p_Z1_new = p_Z2_new = p_Z3_new = p_Z4_new = 9999

zufaelliger_schritt = 0


#Funktion um aus erstellten Plänen alle 1. Schritte auszulesen
def get_first_steps(PlanNr):
    #Alle ersten Schritte werden ausgelesen
    anzahl_plaene = 1 + len(os.listdir(plan_folder))
    plaene = ["Plaenenamen"] * anzahl_plaene
    erste_schritte = [str(PlanNr)] * anzahl_plaene
    for i in range(1,anzahl_plaene):
     plaene[i] = "sas_plan." + str(i)
     #print(plaene[i])

    for i in range(1,anzahl_plaene):
      plan = open(plan_folder / plaene[i], 'r')
      erste_schritte[i] = str(plan.readline().rstrip('\n'))
    return erste_schritte

#Funktion um mit Top-K-Planer bestimmtes Problem-File in Form von "ZielX.pddl" zu lösen und Pläne zu erstellen
def start_top_k_planer(zielpfad):
  command = "/home/familie/symk/fast-downward.py /home/familie/symk/domains/Domain.pddl " + str(zielpfad) + " --search \"symk-bd(plan_selection=top_k_optimal(num_plans=1000))\""
  #print(command)
  os.system(command + "> top_k_planer-output.log")
  return 0

def get_alternative_first_step_for_agent(AgentNr):
    erste_schritte = []
    if(AgentNr == 1):
         if(p_Z1_old > p_Z2_old):
             start_top_k_planer(ziel_pddl_pfad[1])
             update_haeufigkeit_erster_schritt(1)
             erste_schritte.extend(get_first_steps(1))
         elif(p_Z2_old > p_Z1_old):
             start_top_k_planer(ziel_pddl_pfad[2])
             update_haeufigkeit_erster_schritt(2)
             erste_schritte.extend(get_first_steps(2))
         else:
             start_top_k_planer(ziel_pddl_pfad[1])
             update_haeufigkeit_erster_schritt(1)
             erste_schritte.extend(get_first_steps(1))
             print("50-50 Change zwischen den Zielen Agent1 läuft Richtung Ziel1")
    elif(AgentNr == 2):
         if (p_Z3_old > p_Z4_old):
             start_top_k_planer(ziel_pddl_pfad[3])
             update_haeufigkeit_erster_schritt(3)
             erste_schritte.extend(get_first_steps(3))
         elif (p_Z4_old > p_Z3_old):
             start_top_k_planer(ziel_pddl_pfad[4])
             update_haeufigkeit_erster_schritt(4)
             erste_schritte.extend(get_first_steps(4))
         else:
             start_top_k_planer(ziel_pddl_pfad[3])
             update_haeufigkeit_erster_schritt(3)
             erste_schritte.extend(get_first_steps(3))
             print("50-50 Change zwischen den Zielen Agent2 läuft Richtung Ziel3")

    # Alle ersten Schritte werden miteinander verglichen
    treffer = 0
    trefferanzahl = [0] * len(erste_schritte)
    for i in range(1, len(erste_schritte)):
         for k in range(1, len(erste_schritte)):
             if (erste_schritte[i] == erste_schritte[k]):
                 treffer = treffer + 1
         trefferanzahl[i] = treffer
         treffer = 0

    for i in range(1, len(erste_schritte)):
         if (trefferanzahl[i] == max(trefferanzahl)):
             return erste_schritte[i]

def update_haeufigkeit_erster_schritt(ZielNr):
    # erste Schritte und ihre Häufigkeit berechnen und zurückgeben
    erste_schritte = []
    erste_schritte.extend(get_first_steps(ZielNr))
    set_erste_schritte = set(get_first_steps(ZielNr))
    list_erste_schritte = list(set_erste_schritte)
    anzahl_erster_schritt = [0] * len(set_erste_schritte)
    for l in range(len(list_erste_schritte)):
        for m in range(len(erste_schritte)):
            if (list_erste_schritte[l] == erste_schritte[m]):
                anzahl_erster_schritt[l] = anzahl_erster_schritt[l] + 1
        if(ZielNr == 1):
            global z1_anzahl_erster_schritt
            global z1_set_erste_schritte
            global z1_gesamtanzahl_erste_schritte
            z1_gesamtanzahl_erste_schritte = len(get_first_steps(ZielNr)) - 1
            z1_anzahl_erster_schritt = [0] * len(anzahl_erster_schritt)
            z1_set_erste_schritte = ["1"] * len(list_erste_schritte)
            for h in range(len(anzahl_erster_schritt)):
                z1_anzahl_erster_schritt[h] = anzahl_erster_schritt[h]
                z1_set_erste_schritte[h] = list_erste_schritte[h]
        elif(ZielNr == 2):
            global z2_anzahl_erster_schritt
            global z2_set_erste_schritte
            global z2_gesamtanzahl_erste_schritte
            z2_gesamtanzahl_erste_schritte = len(get_first_steps(ZielNr)) - 1
            z2_anzahl_erster_schritt = [0] * len(anzahl_erster_schritt)
            z2_set_erste_schritte = ["2"] * len(list_erste_schritte)
            for h in range(len(anzahl_erster_schritt)):
                z2_anzahl_erster_schritt[h] = anzahl_erster_schritt[h]
                z2_set_erste_schritte[h] = list_erste_schritte[h]
        elif (ZielNr == 3):
            global z3_anzahl_erster_schritt
            global z3_set_erste_schritte
            global z3_gesamtanzahl_erste_schritte
            z3_gesamtanzahl_erste_schritte = len(get_first_steps(ZielNr)) - 1
            z3_anzahl_erster_schritt = [0] * len(anzahl_erster_schritt)
            z3_set_erste_schritte = ["3"] * len(list_erste_schritte)
            for h in range(len(anzahl_erster_schritt)):
                z3_anzahl_erster_schritt[h] = anzahl_erster_schritt[h]
                z3_set_erste_schritte[h] = list_erste_schritte[h]
        elif (ZielNr == 4):
            global z4_anzahl_erster_schritt
            global z4_set_erste_schritte
            global z4_gesamtanzahl_erste_schritte
            z4_gesamtanzahl_erste_schritte = len(get_first_steps(ZielNr)) - 1
            z4_anzahl_erster_schritt = [0] * len(anzahl_erster_schritt)
            z4_set_erste_schritte = ["4"] * len(list_erste_schritte)
            for h in range(len(anzahl_erster_schritt)):
                z4_anzahl_erster_schritt[h] = anzahl_erster_schritt[h]
                z4_set_erste_schritte[h] = list_erste_schritte[h]

def get_best_first_step_for_agent(AgentNr):
    erste_schritte = []
    if(AgentNr == 1):
     for i in range(1,3):
         start_top_k_planer(ziel_pddl_pfad[i])
         #Speichere Lösungen
         if(i==1):
             update_haeufigkeit_erster_schritt(i)
             erste_schritte.extend(get_first_steps(i))
             set1 = set(get_first_steps(i))
         elif(i==2):
             update_haeufigkeit_erster_schritt(i)
             set2 = set(get_first_steps(i))
             set3 = set1.intersection(set2)
             if set3:
                erste_schritte.extend(get_first_steps(i))
                strs = repr(set3)
                eval(strs)
                print(strs[2:-2])
                return strs[2:-2]
             else:
                return False

    elif(AgentNr == 2):
     for i in range(3,5):
         start_top_k_planer(ziel_pddl_pfad[i])
         if(i==3):
             update_haeufigkeit_erster_schritt(i)
             erste_schritte.extend(get_first_steps(i))
             set1 = set(get_first_steps(i))
         elif(i==4):
             update_haeufigkeit_erster_schritt(i)
             set2 = set(get_first_steps(i))
             set3 = set1.intersection(set2)
             if set3:
                erste_schritte.extend(get_first_steps(i))
                strs = repr(set3)
                eval(strs)
                print(strs[2:-2])
                return strs[2:-2]
             else:
                return False

    # Alle ersten Schritte werden miteinander verglichen
    treffer = 0
    trefferanzahl = [0] * len(erste_schritte)
    for i in range(1, len(erste_schritte)):
         for k in range(1, len(erste_schritte)):
             if (erste_schritte[i] == erste_schritte[k]):
                 treffer = treffer + 1
         trefferanzahl[i] = treffer
         treffer = 0

    for i in range(1, len(erste_schritte)):
         if (trefferanzahl[i] == max(trefferanzahl)):
             print(erste_schritte[i])
             return erste_schritte[i]

def aendere_initialzustand(neuer_initialzustand):
    for i in range(1,5):
        pddl_file = open(ziel_pddl_pfad[i], 'r')
        new_pddl_file =open(neuer_ziel_pddl_pfad[i], 'w+')
        for textzeile in pddl_file:
            if (textzeile.find('at-robot') != -1 and not textzeile.find('goal') != -1 ):
                initialzustand = neuer_initialzustand[18:21]
                textzeile = "          (at-robot node" + initialzustand + "))" + '\n'
                new_pddl_file.write(textzeile)
            else:
                new_pddl_file.write(textzeile)
        new_pddl_file.close()
        pddl_file.close()
    for i in range(1,5):
        new_pddl_file = open(neuer_ziel_pddl_pfad[i], 'r')
        pddl_file = open(ziel_pddl_pfad[i], 'w+')
        for textzeile_copy in new_pddl_file:
            pddl_file.write(textzeile_copy)

def mache_schritt(zugerlaubnis):
    print("Zugerlaubnis:", zugerlaubnis)
    bester_erster_schritt_agent1 = get_best_first_step_for_agent(1)
    bester_erster_schritt_agent2 = get_best_first_step_for_agent(2)
    global zufaelliger_schritt

    if(zugerlaubnis == 0):
        if (bester_erster_schritt_agent1 != False):
            print("Agent1 macht Schritt: ", bester_erster_schritt_agent1[18:21])
            aendere_initialzustand(bester_erster_schritt_agent1)
            # Agent2 bekommt für nächsten Zug Zugerlaubnis
            zugerlaubnis = 2
            return zugerlaubnis
        elif(bester_erster_schritt_agent2 != False):
            print("Agent2 macht Schritt: ", bester_erster_schritt_agent2[18:21])
            aendere_initialzustand(bester_erster_schritt_agent2)
            # Agent1 bekommt für nächsten Zug Zugerlaubnis
            zugerlaubnis = 1
            return zugerlaubnis
        else:
            alternativer_erster_schritt_agent1 = get_alternative_first_step_for_agent(1)
            aendere_initialzustand(alternativer_erster_schritt_agent1)
            print("Beide Agenten haben keinen gemeinsamen 1. Schritt")
            print("Daher macht Agent 1 einen alternativen Schritt in Richtung eines Ziels")
            zufaelliger_schritt = 1
            # Agent2 bekommt für nächsten Zug Zugerlaubnis
            zugerlaubnis = 2
            return zugerlaubnis

    if(zugerlaubnis == 1):
        if (p_Z1_old == 1 or p_Z2_old == 1):
            alternativer_erster_schritt_agent1 = get_alternative_first_step_for_agent(1)
            aendere_initialzustand(alternativer_erster_schritt_agent1)
            print("Agent 1 weiß das wahre Ziel und zieht dort hin")
            # Agent2 bekommt für nächsten Zug Zugerlaubnis
            zugerlaubnis = 2
            return zugerlaubnis
        elif(bester_erster_schritt_agent1 != False):
            print("Agent1 macht Schritt: ", bester_erster_schritt_agent1[18:21])
            aendere_initialzustand(bester_erster_schritt_agent1)
            # Agent2 bekommt für nächsten Zug Zugerlaubnis
            zugerlaubnis = 2
            return zugerlaubnis
        elif (p_Z3_old == 1 or p_Z4_old == 1):
            alternativer_erster_schritt_agent2 = get_alternative_first_step_for_agent(2)
            aendere_initialzustand(alternativer_erster_schritt_agent2)
            print("Agent 2 weiß das wahre Ziel und zieht dort hin")
            # Agent1 bekommt für nächsten Zug Zugerlaubnis
            zugerlaubnis = 1
            return zugerlaubnis
        elif(bester_erster_schritt_agent2 != False):
            print("Agent2 macht Schritt: ", bester_erster_schritt_agent2[18:21])
            aendere_initialzustand(bester_erster_schritt_agent2)
            # Agent1 bekommt für nächsten Zug Zugerlaubnis
            zugerlaubnis = 1
            return zugerlaubnis
        else:
            alternativer_erster_schritt_agent1 = get_alternative_first_step_for_agent(1)
            aendere_initialzustand(alternativer_erster_schritt_agent1)
            print("Beide Agenten haben keinen gemeinsamen 1. Schritt")
            print("Daher macht Agent 1 einen alternativen Schritt in Richtung eines Ziels")
            zufaelliger_schritt = 1
            # Agent2 bekommt für nächsten Zug Zugerlaubnis
            zugerlaubnis = 2
            return zugerlaubnis

    if(zugerlaubnis == 2):
        if (p_Z3_old == 1 or p_Z4_old == 1):
            alternativer_erster_schritt_agent2 = get_alternative_first_step_for_agent(2)
            aendere_initialzustand(alternativer_erster_schritt_agent2)
            print("Agent 2 weiß das wahre Ziel und zieht dort hin")
            # Agent1 bekommt für nächsten Zug Zugerlaubnis
            zugerlaubnis = 1
            return zugerlaubnis
        elif(bester_erster_schritt_agent2 != False):
            print("Agent2 macht Schritt: ", bester_erster_schritt_agent2[18:21])
            aendere_initialzustand(bester_erster_schritt_agent2)
            # Agent1 bekommt für nächsten Zug Zugerlaubnis
            zugerlaubnis = 1
            return zugerlaubnis
        if (p_Z1_old == 1 or p_Z2_old == 1):
            alternativer_erster_schritt_agent1 = get_alternative_first_step_for_agent(1)
            aendere_initialzustand(alternativer_erster_schritt_agent1)
            print("Agent 1 weiß das wahre Ziel und zieht dort hin")
            # Agent2 bekommt für nächsten Zug Zugerlaubnis
            zugerlaubnis = 2
            return zugerlaubnis
        elif(bester_erster_schritt_agent1 != False):
            print("Agent1 macht Schritt: ", bester_erster_schritt_agent1[18:21])
            aendere_initialzustand(bester_erster_schritt_agent1)
            # Agent2 bekommt für nächsten Zug Zugerlaubnis
            zugerlaubnis = 2
            return zugerlaubnis
        else:
            alternativer_erster_schritt_agent1 = get_alternative_first_step_for_agent(1)
            aendere_initialzustand(alternativer_erster_schritt_agent1)
            print("Beide Agenten haben keinen gemeinsamen 1. Schritt")
            print("Daher macht Agent 1 einen alternativen Schritt in Richtung eines Ziels")
            zufaelliger_schritt = 1
            # Agent2 bekommt für nächsten Zug Zugerlaubnis
            zugerlaubnis = 2
            return zugerlaubnis

def get_initialzustand():
    pddl_file = open(ziel_pddl_pfad[1], 'r')
    for textzeile in pddl_file:
        if (textzeile.find('at-robot') != -1 and not textzeile.find('goal') != -1):
            pddl_file.close()
            return textzeile[24:27]

def schritt_beobachten(AgentNr,old_initialzustand):
    new_initialzustand = get_initialzustand()
    step = "(move node" + old_initialzustand + " node"+ new_initialzustand +")"

    if(AgentNr == 1):
      print("Agent 1 beobachtet und passt Wahrscheinlichkeiten an:")
      global p_Z1_old
      global p_Z2_old
      global p_Z1_new
      global p_Z2_new

      merker = 0
      for i in range(len(z1_anzahl_erster_schritt)):
                if(step == z1_set_erste_schritte[i]):
                    for n in range(len(z2_anzahl_erster_schritt)):
                        if(step == z2_set_erste_schritte[n]):
                            p_Z1_new = (p_Z1_old * (z1_anzahl_erster_schritt[i] / z1_gesamtanzahl_erste_schritte)) / (
                                        (p_Z1_old * (z1_anzahl_erster_schritt[i] / z1_gesamtanzahl_erste_schritte)) + (
                                            p_Z2_old * (z2_anzahl_erster_schritt[n] / z2_gesamtanzahl_erste_schritte)))
                            merker = 1
                        elif(step != z2_set_erste_schritte[n] and n + 1 == len(z2_anzahl_erster_schritt) and merker == 0):
                            p_Z1_new = (p_Z1_old * (z1_anzahl_erster_schritt[i] / z1_gesamtanzahl_erste_schritte)) / (
                                    (p_Z1_old * (z1_anzahl_erster_schritt[i] / z1_gesamtanzahl_erste_schritte)) + (
                                    p_Z2_old * 0))
                            merker = 1
                elif (step != z1_set_erste_schritte[i] and i + 1 == len(z1_anzahl_erster_schritt) and merker == 0):
                    p_Z1_new = 0

      merker = 0
      for i in range(len(z2_anzahl_erster_schritt)):
                if(step == z2_set_erste_schritte[i]):
                    for n in range(len(z1_anzahl_erster_schritt)):
                        if(step == z1_set_erste_schritte[n]):
                            p_Z2_new = (p_Z2_old * (z2_anzahl_erster_schritt[i] / z2_gesamtanzahl_erste_schritte)) / (
                                        (p_Z2_old * (z2_anzahl_erster_schritt[i] / z2_gesamtanzahl_erste_schritte)) + (
                                            p_Z1_old * (z1_anzahl_erster_schritt[n] / z1_gesamtanzahl_erste_schritte)))
                            merker = 1
                        elif(step != z1_set_erste_schritte[n] and n + 1 == len(z1_anzahl_erster_schritt) and merker == 0):
                            p_Z2_new = (p_Z2_old * (z2_anzahl_erster_schritt[i] / z2_gesamtanzahl_erste_schritte)) / (
                                    (p_Z2_old * (z2_anzahl_erster_schritt[i] / z2_gesamtanzahl_erste_schritte)) + (
                                    p_Z1_old * 0))
                            merker = 1
                elif(step != z2_set_erste_schritte[i] and i + 1 == len(z2_anzahl_erster_schritt) and merker == 0):
                    p_Z2_new = 0
      global zufaelliger_schritt
      if(zufaelliger_schritt == 1):
          print("Wahrscheinlichkeiten bleiben gleich wegen zufälligem Schritt")
          print("P(Ziel1):", p_Z1_old)
          print("P(Ziel2):", p_Z2_old)
          zufaelliger_schritt = 0
      else:
          print("P(Ziel1):", p_Z1_new)
          print("P(Ziel2):", p_Z2_new)
          p_Z1_old = p_Z1_new
          p_Z2_old = p_Z2_new

    if(AgentNr == 2):
        print("Agent 2 beobachtet und passt Wahrscheinlichkeiten an:")
        global p_Z3_old
        global p_Z4_old
        global p_Z3_new
        global p_Z4_new
        merker = 0
        for i in range(len(z3_anzahl_erster_schritt)):
            if (step == z3_set_erste_schritte[i]):
                for n in range(len(z4_anzahl_erster_schritt)):
                    if (step == z4_set_erste_schritte[n]):
                        p_Z3_new = (p_Z3_old * (z3_anzahl_erster_schritt[i] / z3_gesamtanzahl_erste_schritte)) / (
                                (p_Z3_old * (z3_anzahl_erster_schritt[i] / z3_gesamtanzahl_erste_schritte)) + (
                                p_Z4_old * (z4_anzahl_erster_schritt[n] / z4_gesamtanzahl_erste_schritte)))
                        merker = 1
                    elif (step != z4_set_erste_schritte[n] and n + 1 == len(z4_anzahl_erster_schritt) and merker == 0):
                        p_Z3_new = (p_Z3_old * (z3_anzahl_erster_schritt[i] / z3_gesamtanzahl_erste_schritte)) / (
                                (p_Z3_old * (z3_anzahl_erster_schritt[i] / z3_gesamtanzahl_erste_schritte)) + (
                                p_Z4_old * 0))
                        merker = 1
            elif (step != z3_set_erste_schritte[i] and i + 1 == len(z3_anzahl_erster_schritt) and merker == 0):
                p_Z3_new = 0

        merker = 0
        for i in range(len(z4_anzahl_erster_schritt)):
            if (step == z4_set_erste_schritte[i]):
                for n in range(len(z3_anzahl_erster_schritt)):
                    if (step == z3_set_erste_schritte[n]):
                        p_Z4_new = (p_Z4_old * (z4_anzahl_erster_schritt[i] / z4_gesamtanzahl_erste_schritte)) / (
                                (p_Z4_old * (z4_anzahl_erster_schritt[i] / z4_gesamtanzahl_erste_schritte)) + (
                                p_Z3_old * (z3_anzahl_erster_schritt[n] / z3_gesamtanzahl_erste_schritte)))
                        merker = 1
                    elif (step != z3_set_erste_schritte[n] and n + 1 == len(z3_anzahl_erster_schritt) and merker == 0):
                        p_Z4_new = (p_Z4_old * (z4_anzahl_erster_schritt[i] / z4_gesamtanzahl_erste_schritte)) / (
                                (p_Z4_old * (z4_anzahl_erster_schritt[i] / z4_gesamtanzahl_erste_schritte)) + (
                                p_Z3_old * 0))
                        merker = 1
            elif (step != z4_set_erste_schritte[i] and i + 1 == len(z4_anzahl_erster_schritt) and merker == 0):
                p_Z4_new = 0

        if (zufaelliger_schritt == 1):
            print("Wahrscheinlichkeiten bleiben gleich wegen zufälligem Schritt")
            print("P(Ziel3):", p_Z3_old)
            print("P(Ziel4):", p_Z4_old)
            zufaelliger_schritt = 0
        else:
            print("P(Ziel3):", p_Z3_new)
            print("P(Ziel4):", p_Z4_new)
            p_Z3_old = p_Z3_new
            p_Z4_old = p_Z4_new


    return new_initialzustand, p_Z1_old, p_Z2_old, p_Z3_old, p_Z4_old

def get_cost(GemeinsamesZiel):
    i = GemeinsamesZiel
    start_top_k_planer(ziel_pddl_pfad[i])
    plan_pfad = plan_folder / "sas_plan.1"
    if plan_pfad.is_file():
        Plan = open(plan_pfad, "r")
        for textzeile in Plan:
            if (textzeile.find('cost') != -1):
                cost = textzeile[9]
                print(cost)
    else:
        cost = 0 #keine Pläne
        print("Es gibt keinen Plan")
    return cost





