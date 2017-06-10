import base
from simulation import Simulation

class Trajectoire(object):

    def __init__(self):
        self.trajectoires = base.EmptyListDict()

    def mettreAJourTrajectoires(self, simulation):
        for personne in simulation.ensemble_personnes:
            if not personne.estSortie():
                self.trajectoires[personne].append(personne.position)
        return Simulation.AUCUN

    def genererXYArrays(self):
        return map(base.unzip, self.trajectoires.values())
