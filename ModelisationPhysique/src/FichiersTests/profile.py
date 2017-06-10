import sys
sys.path.append('..')
from convertir_json_python import convertirJsonPython
from traitement import RecuperationDeDonnees, TraitementDeDonnees
from affichage import Afficheur
import cProfile

NOMBRE_SIMULATION = 2
configuration = convertirJsonPython(
    '../FichiersConfiguration/MPSTAR.json')

def toProfile():
    for _ in range(NOMBRE_SIMULATION):
        recuperation = RecuperationDeDonnees(
            configuration,
            arreter_apres_temps=True,
            temps_maximal=10)
        recuperation.lancer()


cProfile.run('toProfile()', filename='MPSTARTimeStats.stat')
