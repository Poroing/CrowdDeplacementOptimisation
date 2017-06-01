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

configuration = convertirJsonPython(
    '../FichiersConfiguration/MPSI2_obstacle_devant_porte.json')
recuperation = RecuperationDeDonnees(
    configuration,
    arreter_apres_temps=True,
    temps_maximal=20,
    action_mise_a_jour_secondaire=afficheur.dessinerEspaceEtAttendre)

recuperation.lancer()
