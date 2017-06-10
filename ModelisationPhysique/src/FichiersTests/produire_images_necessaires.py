import sys
sys.path.append('..')
from convertir_json_python import convertirJsonPython
from traitement import RecuperationDeDonnees, TraitementDeDonnees
from affichage import Afficheur, TraceurTrajectoire
from base import EnsembleRappelleRenvoyantCommande
from personne import Personne
import test_point_suivre
import matplotlib.pyplot as plt

traceur_trajectoire = TraceurTrajectoire()

current_figure = plt.figure()

def avoirRecuperation(nom_configuration, mise_a_jour):
    configuration = convertirJsonPython(nom_configuration)

    return RecuperationDeDonnees(
        configuration,
        arreter_apres_temps=True,
        temps_maximal=15,
        action_mise_a_jour_secondaire=mise_a_jour)

def avoirNouvelleFigure(recuperation):
    current_figure = plt.figure()
    plt.xlim((
        recuperation.simulation.espace.lieu_ferme.position.x,
        recuperation.simulation.espace.lieu_ferme.largeur
            + recuperation.simulation.espace.lieu_ferme.position.x))
    plt.ylim((
        recuperation.simulation.espace.lieu_ferme.position.y,
        recuperation.simulation.espace.lieu_ferme.hauteur
            + recuperation.simulation.espace.lieu_ferme.position.y))

def sauvegarderTrajectoire(nom_fichier, nom_configuration, test_direction, background=None):
    Personne.TEST_DIRECTION = test_direction
    traceur_trajectoire = TraceurTrajectoire()
    recuperation = avoirRecuperation(
        nom_configuration,
        traceur_trajectoire.mettreAJourTrajectoires)
    recuperation.lancer()
    avoirNouvelleFigure(recuperation)
    traceur_trajectoire.tracerTrajectoires()
    plt.savefig(nom_fichier)


#Trajectoires test proximite
sauvegarderTrajectoire(
    '../../resultats/TrajectoireTestProximiteMPSTARTroisPersonnes.png',
    '../FichiersConfiguration/MPSTAR_trois_personne.json',
    test_point_suivre.TestProximite)

#Trajectoires test dichotomie
sauvegarderTrajectoire(
    '../../resultats/TrajectoireTestDichotomieMPSTARTroisPersonnes.png',
    '../FichiersConfiguration/MPSTAR_trois_personne.json',
    test_point_suivre.TestDichotomieCompactageObstacle)

#Trajectoire obstacle devant porte dichotomie
sauvegarderTrajectoire(
    '../../resultats/TrajectoireTestDichotomieMPSI2TroisPersonne.png',
    '../FichiersConfiguration/salle_vide_obstacle_devant_porte_trois_personnes.json',
    test_point_suivre.TestDichotomieCompactageObstacle)
