import sys
sys.path.append('..')
from convertir_json_python import convertirJsonPython
from traitement import RecuperationDeDonnees, TraitementDeDonnees
from affichage import Afficheur

afficheur = Afficheur()

configuration = convertirJsonPython(
    '../FichiersConfiguration/salle_en_Y.json')
recuperation = RecuperationDeDonnees(
    configuration,
    arreter_apres_temps=True,
    temps_maximal=15,
    action_mise_a_jour_secondaire=afficheur.dessinerEspaceEtAttendre)

recuperation.lancer()
