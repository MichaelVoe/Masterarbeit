import solve_pddl
from solve_pddl import mache_schritt, schritt_beobachten, get_cost
from make_pddl import make_lab
from visualize_pddl import draw_lab, draw_lab_wait
from pathlib import Path

data_folder = Path("/home/familie/symk/repo/")
auswertung_pddl_pfad = data_folder / "Auswertung.txt"
open(auswertung_pddl_pfad, 'w').close()
auswertungs_datei = open(auswertung_pddl_pfad,"a")
auswertungs_datei.write(("Nr;Resultat; Gemachte Schritte; Optimale Anzahl Schritte; Gemeinsames Ziel; Einzelnes Ziel Agent 1; Einzelnes Ziel Agent 2; Labyrinth\n"))

for i in range(1,101):
    solve_pddl.p_Z1_old = 0.5
    solve_pddl.p_Z2_old = 0.5
    solve_pddl.p_Z3_old = 0.5
    solve_pddl.p_Z4_old = 0.5
    feld, ziel1, ziel2, ziel3, ziel4 = make_lab()
    if(ziel1 == ziel3):
        goal_init = ziel1
        GemeinsamesZiel = 1
        alternativ_goal_agent1 = ziel2
        alternativ_goal_agent2 = ziel4
    elif(ziel1 == ziel4):
        goal_init = ziel1
        GemeinsamesZiel = 1
        alternativ_goal_agent1 = ziel2
        alternativ_goal_agent2 = ziel3
    elif(ziel2 == ziel3):
        goal_init = ziel2
        GemeinsamesZiel = 2
        alternativ_goal_agent1 = ziel1
        alternativ_goal_agent2 = ziel4
    else:
        goal_init = ziel2
        GemeinsamesZiel = 2
        alternativ_goal_agent1 = ziel1
        alternativ_goal_agent2 = ziel3
    cost = get_cost(GemeinsamesZiel)
    draw_lab()
    turn_token = mache_schritt(0) # 0 = der Token der zum Zug berechtigt ist noch nicht vergeben. Nachdem er einmal aufgenommen wurde wechseln sich die Agenten ab
    steps_made = 1
    old_init, p_Z1, p_Z2, p_Z3, p_Z4 = schritt_beobachten(turn_token,"3-3") # 3-3 = Startpostion/Startinitialzustand
    while (goal_init != old_init): #Ziel erreicht als Abbruchkriterium
    #while(goal_init != old_init or (p_Z1 != 1 and p_Z2 != 1) or (p_Z3 != 1 and p_Z4 != 1)): #Ziel erreichen und Wahrscheinlichkeiten 100% als Abbruchkriterium
        draw_lab()
        turn_token = mache_schritt(turn_token)
        steps_made = steps_made + 1
        old_init, p_Z1, p_Z2, p_Z3, p_Z4 = schritt_beobachten(turn_token,old_init)
        resultat = "Done"
        if(steps_made >= 30): #Abbruch bei 30 Zügen
            resultat = "Failed"
            break
    #Schreibe Ergebnis an das Ende des Protokolls
    datenstring = str(i)+ " ; " + resultat + " ; " + str(steps_made) + " ; " + str(cost) + " ; " + goal_init + " ; " + str(alternativ_goal_agent1) + " ; " + str(alternativ_goal_agent2) + " ; " + str(feld) + "\n"
    auswertungs_datei.write(datenstring)
    draw_lab()

