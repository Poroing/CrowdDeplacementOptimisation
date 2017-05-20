import sys
sys.path.append('..')
from convertir_json_python import convertirJsonPython
from traitement import RecuperationDeDonnees, TraitementDeDonnees
import matplotlib.pyplot as plt
from aide_etude import genererResultatDeNSimulation

def recupererNDebitMoyenPourConfiguration(configuration, n, afficher_numero_simulation=False):
    debits_moyens = []
    for numero_simulation, recuperation in enumerate(genererResultatDeNSimulation(configuration, n)):
        if afficher_numero_simulation:
            print('Simulation', numero_simulation)
        traitement = TraitementDeDonnees(recuperation.temps_de_sortie)
        debits_moyens.append(traitement.avoirDebitMoyen())
    return debits_moyens

configuration_obstacle = convertirJsonPython(
    '../FichiersConfiguration/MPSI2_obstacle_devant_porte.json')
configuration_sans_obstacle = convertirJsonPython(
    '../FichiersConfiguration/MPSI2.json')

debits_moyens_obstacle = recupererNDebitMoyenPourConfiguration(
    configuration_obstacle,
    100,
    afficher_numero_simulation=True)
debits_moyens_sans_obstacle = recupererNDebitMoyenPourConfiguration(
    configuration_sans_obstacle,
    100,
    afficher_numero_simulation=True)

plt.subplot(121)
plt.hist(debits_moyens_obstacle, 20, range=(0, 13))
plt.subplot(122)
plt.hist(debits_moyens_sans_obstacle, 20, range=(0, 13))
plt.show()
