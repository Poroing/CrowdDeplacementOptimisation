import sys
sys.path.append('..')
from convertir_json_python import convertirJsonPython
from traitement import RecuperationDeDonnees, TraitementDeDonnees
from affichage import Afficheur
from personne import Personne
import test_point_suivre

Personne.TEST_DIRECTION = test_point_suivre.TestGradientLargeurQuatreDirections

afficheur = Afficheur(debug=False)

configuration = convertirJsonPython(
    '../FichiersConfiguration/MPSTAR.json')
recuperation = RecuperationDeDonnees(
    configuration,
    arreter_apres_temps=True,
    temps_maximal=15,
    action_mise_a_jour_secondaire=afficheur.dessinerEspaceEtAttendre)

recuperation.lancer()
