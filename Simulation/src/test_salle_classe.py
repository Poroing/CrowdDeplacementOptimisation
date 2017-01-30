from simulation_propre import ConstructeurSimulation, Simulation
from convertir_json_python import convertirJsonPython
from traitement_propre import RecuperationDeDonnees
import matplotlib.pyplot as plt
from source_personne import Source
from affichage import Afficheur

afficheur = Afficheur()

configuration = convertirJsonPython('./configuration_MPSI2.json')
recuperation = RecuperationDeDonnees(configuration, temps_maximal=20, action_mise_a_jour_secondaire=afficheur.dessinerEspaceEtAttendre)
#recuperation.simulation.sources.append(Source(recuperation.simulation.espace, Vec2d(500, 750), 0.5))
        
recuperation.lancer()
plt.plot([0] + recuperation.temps_de_sortie, list(range(len(recuperation.temps_de_sortie) + 1)))
plt.show()
