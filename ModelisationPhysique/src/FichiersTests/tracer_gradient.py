import sys
sys.path.append('..')
from convertir_json_python import convertirJsonPython
from traitement import RecuperationDeDonnees
from affichage import afficherChampGradient
from test_point_suivre import TestGradient

configuration = convertirJsonPython(
    '../FichiersConfiguration/salle_en_T.json')
recuperation = RecuperationDeDonnees(
    configuration,
    arreter_apres_temps=True,
    temps_maximal=15)

premier_champ = next(iter(TestGradient.treillis_interet.values()))
afficherChampGradient(premier_champ)
