import sys
sys.path.append('..')
import threaded_simulations
from convertir_json_python import convertirJsonPython
from traitement import RecuperationDeDonnees, TraitementDeDonnees
import matplotlib.pyplot as plt
from aide_etude import genererResultatDeNSimulation


if __name__ == '__main__':
    debits_moyens_obstacle = []
    debits_moyens_sans_obstacle = []
    configuration1 = convertirJsonPython(
        '../FichiersConfiguration/salle_vide.json')
    configuration2 = convertirJsonPython(
        '../FichiersConfiguration/salle_vide_avec_obstacle.json')

    for debit in threaded_simulations.avoirDebitsMoyenSimulation(
            10,
            configuration1,2):
        debits_moyens_obstacle.append(debit)
        
    for debit in threaded_simulations.avoirDebitsMoyenSimulation(
            10,
            configuration2,2):
        debits_moyens_obstacle.append(debit)
        
        
plt.subplot(121)
plt.hist(debits_moyens_obstacle, 20, range=(0, 13))
plt.subplot(122)
plt.hist(debits_moyens_sans_obstacle, 20, range=(0, 13))
plt.show()

