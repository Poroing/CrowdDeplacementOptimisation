import sys
sys.path.append('..')
from convertir_json_python import convertirJsonPython
from traitement import RecuperationDeDonnees, TraitementDeDonnees
from affichage import Afficheur, TraceurTrajectoire
from base import EnsembleRappelleRenvoyantCommande

afficheur = Afficheur()
traceur_trajectoire = TraceurTrajectoire()

mise_a_jour = EnsembleRappelleRenvoyantCommande()
mise_a_jour.ajouter(afficheur.dessinerEspaceEtAttendre)
mise_a_jour.ajouter(traceur_trajectoire.mettreAJourTrajectoires)

configuration = convertirJsonPython(
    '../FichiersConfiguration/salle_en_T.json')

recuperation = RecuperationDeDonnees(
    configuration,
    arreter_apres_temps=True,
    temps_maximal=15,
    action_mise_a_jour_secondaire=mise_a_jour)

recuperation.lancer()
traceur_trajectoire.afficherTrajectoires()
