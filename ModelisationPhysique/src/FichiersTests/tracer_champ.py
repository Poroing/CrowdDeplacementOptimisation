import sys
sys.path.append('..')
from convertir_json_python import convertirJsonPython
from traitement import RecuperationDeDonnees
from affichage import afficherChampVectorielle
import test_point_suivre
from personne import Personne

Personne.TEST_DIRECTION = test_point_suivre.TestChampVecteurQuatreDirections

configuration = convertirJsonPython(
    '../FichiersConfiguration/MPSTAR.json')
recuperation = RecuperationDeDonnees(
    configuration,
    arreter_apres_temps=True,
    temps_maximal=15)

premier_champ = next(iter(test_point_suivre.TestChampVecteur.champs.values()))
afficherChampVectorielle(premier_champ)
