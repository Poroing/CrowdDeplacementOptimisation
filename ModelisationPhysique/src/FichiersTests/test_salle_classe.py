import sys
sys.path.append('..')
from convertir_json_python import convertirJsonPython
from traitement import RecuperationDeDonnees, TraitementDeDonnees
import matplotlib.pyplot as plt
from source_personne import Source
from affichage import Afficheur
from random import randint
from mpl_toolkits.mplot3d import Axes3D     


configuration = convertirJsonPython('../FichiersConfiguration/MPSTAR.json')
#recuperation.simulation.sources.append(Source(recuperation.simulation.espace, Vec2d(500, 750), 0.5))
        

afficheur = Afficheur()
recuperation = RecuperationDeDonnees(configuration, arreter_apres_temps=True,
        temps_maximal=15,
        action_mise_a_jour_secondaire = afficheur.dessinerEspaceEtAttendre)


recuperation.lancer()
