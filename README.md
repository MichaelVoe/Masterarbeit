# Masterarbeit

Das Ziel dieser Arbeit ist es Erkenntnisse für einen möglichen neuen Ansatz zu gewinnen, 
mit dem sich Multi-Agenten Pfadfindungs-Probleme mit Hilfe von Zielerkennung lösen lassen. 
Für diesen Erkenntnisgewinn wird ein spezielles MAPF-Problem
konstruiert bei dem zwei Agenten einen gemeinsamen Spielstein durch abwechselndes Ziehen 
auf ein gemeinsames Ziel ziehen sollen. Die Agenten besitzen dabei das
Wissen über eine Menge von möglichen Zielzuständen und haben das zusätzliche
Wissen, dass einer dieser Zielzustände der gemeinsame Zielzustand ist auf den der
Spielstein bewegt werden soll. Durch eine geschickte Abfolge von Zügen und Beobachtungen sollen die Agenten Gewissheit über das gemeinsame Ziel erlangen und das
MAPF-Problem lösen indem sie den Spielstein auf das gemeinsame Ziel bewegen.

Beschreibung der Dateien:

- main.py: Ermöglicht durch Aufruf der Funktionen ein automatsiertes Lösen von beliebig vielen MAPF-Problemen 
- make_pddl.py: Generiert zufälliges MAPF-Problem durch die Manipulation von PDDL Problem-Dateien
- visualize_pddl.py: Erzeugt grafische Ausgabe des MAPF-Problems 
- solve_pddl.py: Implementierung des Algorithmus für die Lösung generierter MAPF-Probleme

- Domain.pddl: Domain Datei für MAPF-Problem
- Sample.pddl: Problem Datei für MAPF-Problem wird von make_pddl.py verwendet um randomisierte MAPF-Probleme zu generieren

- top_k_optimal_selector.cc: Eigner Selektor für Top-K-Planer der die Plangenerierung nach dem Erstellen aller optimaler Pläne abbricht
