import sys
sys.path.append('..')
from simulation import ConstructeurSimulation, Simulation
from convertir_json_python import convertirJsonPython
from traitement import RecuperationDeDonnees
import matplotlib.pyplot as plt
from source_personne import Source
from affichage import Afficheur

afficheur = Afficheur()

configuration = convertirJsonPython('../FichiersConfiguration/configuration_MPSI2_obstacle_devant_porte.json')
recuperation = RecuperationDeDonnees(configuration, temps_maximal=20, action_mise_a_jour_secondaire=afficheur.dessinerEspaceEtAttendre)
#recuperation.simulation.sources.append(Source(recuperation.simulation.espace, Vec2d(500, 750), 0.5))
        
recuperation.lancer()
#plt.plot([0] + recuperation.temps_de_sortie, list(range(len(recuperation.temps_de_sortie) + 1)))
#plt.show()
