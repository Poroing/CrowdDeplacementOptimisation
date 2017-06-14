import sys
sys.path.append('..')
from convertir_json_python import convertirJsonPython
from traitement import RecuperationDeDonnees, TraitementDeDonnees
from affichage import Afficheur

configuration = convertirJsonPython(
    '../FichiersConfiguration/salle_efficacite.json')
recuperation = RecuperationDeDonnees(
    configuration,
    arreter_apres_temps=False)

recuperation.lancer()
