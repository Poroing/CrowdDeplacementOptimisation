import sys
sys.path.append('..')
from convertir_json_python import convertirJsonPython
from traitement import RecuperationDeDonnees
from affichage import afficherChampGradient
import test_point_suivre
from personne import Personne

Personne.TEST_DIRECTION = test_point_suivre.TestGradientLargeurHuitDirections

configuration = convertirJsonPython(
    '../FichiersConfiguration/MPSTAR.json')
recuperation = RecuperationDeDonnees(
    configuration,
    arreter_apres_temps=True,
    temps_maximal=15)

premier_champ = next(iter(test_point_suivre.TestGradient.treillis_interet.values()))
afficherChampGradient(premier_champ)
