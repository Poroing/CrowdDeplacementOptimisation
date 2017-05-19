import sys
sys.path.append('..')
from traitement import RecuperationDeDonnees

def genererResultatDeNSimulation(configuration, n, temps_maximal_simulation=15):
    for _ in range(n):
        recuperation = RecuperationDeDonnees(
            configuration,
            arreter_apres_temps=True,
            temps_maximal=temps_maximal_simulation,
            arreter_apres_sortie=True)
        recuperation.lancer()
        yield recuperation
