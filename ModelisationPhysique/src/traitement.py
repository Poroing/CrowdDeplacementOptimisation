from functools import partial
from matplotlib.pyplot import plot
from simulation import Simulation, ConstructeurSimulation

class RecuperationDeDonnees(object):
    
    def __init__(self, configuration_simulation, arreter_apres_temps=True, temps_maximal=0, action_mise_a_jour_secondaire=None):
        if action_mise_a_jour_secondaire is None:
            action_mise_a_jour_secondaire = lambda simulation: Simulation.AUCUN

        self.temps_de_sortie = []

        self.temps_maximal = temps_maximal
        self.arreter_apres_temps = arreter_apres_temps

        constructeur_simulation = ConstructeurSimulation(configuration_simulation, self.ajouterTempsSortie)
        self.simulation = constructeur_simulation.simulation

        self.action_mise_a_jour_secondaire = action_mise_a_jour_secondaire
        self.simulation.action_mise_a_jour = self.actionMiseAJour

    def lancer(self):
        self.simulation.lancer()

    def ajouterTempsSortie(self, temps):
        self.temps_de_sortie.append(temps)

    def avoirNombrePersonneSortie(self):
        return len(self.temps_de_sortie)

    def actionMiseAJour(self, simulation):
        commandes = self.action_mise_a_jour_secondaire(simulation)
        if self.arreter_apres_temps and simulation.temps_depuis_lancement > self.temps_maximal:
            commandes = commandes | Simulation.ARRET
        return commandes
        
class TraitementDeDonnees(object):
    
    
    def __init__(self, temps_de_sortie):
        
        self.temps_de_sortie = temps_de_sortie
        self.nombre = len(self.temps_de_sortie)
    
    def personnes_en_fonction_du_temps(self):
        plt.plot([0] + self.temps_de_sortie, list(range(len(self.temps_de_sortie)+1)))
    
    def debit_ordre_premier(self):
        derivee = [0]
        for x in range (1,self.nombre) :
            print(self.temps_de_sortie[x] - self.temps_de_sortie[x-1])
            derivee.append(1/(self.temps_de_sortie[x] - self.temps_de_sortie[x-1]))
            
        return derivee + [0]
        

    def debit_ordre_quatre(self):
        derivee = [0]
        derivee.append((1/self.temps_de_sortie[1]-self.temps_de_sortie[0]))
        for x in range (2, self.nombre - 2):
            
            derivee.append(- 12/( -self.temps_de_sortie[x-2] + 8 * self.temps_de_sortie[x-1] - 8 * self.temps_de_sortie[x+1] + self.temps_de_sortie[x+2]))
        
        derivee.append(1/(self.temps_de_sortie[self.nombre-2]-self.temps_de_sortie[self.nombre-3]))
        derivee.append(1/(self.temps_de_sortie[self.nombre-1]-self.temps_de_sortie[self.nombre-2]))
        return derivee + [0]

    def avoirDebitMoyen(self):
        ensemble_debits = self.debit_ordre_quatre()
        return sum(ensemble_debits) / len(ensemble_debits)
        
