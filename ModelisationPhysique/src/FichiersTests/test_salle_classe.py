import sys
sys.path.append('..')
from convertir_json_python import convertirJsonPython
from traitement import RecuperationDeDonnees, TraitementDeDonnees
import matplotlib.pyplot as plt
from source_personne import Source
from affichage import Afficheur
from random import randint
from mpl_toolkits.mplot3d import Axes3D

afficheur = Afficheur()

configuration = convertirJsonPython('../FichiersConfiguration/MPSTAR_avec_obstacle.json')


recuperation = RecuperationDeDonnees(configuration, temps_maximal=10, action_mise_a_jour_secondaire=afficheur.dessinerEspaceEtAttendre)
#recuperation.simulation.sources.append(Source(recuperation.simulation.espace, Vec2d(500, 750), 0.5))
        
recuperation.lancer()
traitement = TraitementDeDonnees(recuperation.temps_de_sortie)
traitement.avoirDebitMoyen()

##
fig = plt.figure()  
plt.plot(ord, sortie)
plt.show()
