import sys
sys.path.append('..')
from convertir_json_python import convertirJsonPython
from traitement import RecuperationDeDonnees, TraitementDeDonnees
import matplotlib.pyplot as plt
from source_personne import Source
from affichage import Afficheur
from random import randint
from mpl_toolkits.mplot3d import Axes3D


configuration = convertirJsonPython('../FichiersConfiguration/configuration_MPSI2_obstacle_devant_porte.json')
#recuperation.simulation.sources.append(Source(recuperation.simulation.espace, Vec2d(500, 750), 0.5))
        
data = []
for numero_simumation in range(50):
    print(f'Simulation {numero_simumation}')
    recuperation = RecuperationDeDonnees(configuration, arreter_apres_temps=True,
        temps_maximal=15,
        arreter_apres_sortie=True)
    recuperation.lancer()
    traitement = TraitementDeDonnees(recuperation.temps_de_sortie)
    data.append(traitement.avoirDebitMoyen())

configuration = convertirJsonPython('

plt.hist(data, 20)
plt.show()
