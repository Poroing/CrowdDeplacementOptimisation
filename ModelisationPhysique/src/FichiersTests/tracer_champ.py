import sys
sys.path.append('..')
from convertir_json_python import convertirJsonPython
from traitement import RecuperationDeDonnees
from affichage import afficherChampVectorielle
from test_point_suivre import TestChampVecteur

configuration = convertirJsonPython(
    '../FichiersConfiguration/salle_en_T.json')
recuperation = RecuperationDeDonnees(
    configuration,
    arreter_apres_temps=True,
    temps_maximal=15)

premier_champ = next(iter(TestChampVecteur.champs.values()))
afficherChampVectorielle(premier_champ)
