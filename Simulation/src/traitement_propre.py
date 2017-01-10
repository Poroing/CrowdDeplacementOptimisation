from functools import partial
from matplotlib.pyplot import plot
from simulation_propre import Simulation, ConstructeurSimulation

##
class RecuperationDeDonnees(object):
    
    def __init__(self, configuration_simulation, temps_maximal, action_mise_a_jour_secondaire=None):
        if action_mise_a_jour_secondaire is None:
            action_mise_a_jour_secondaire = lambda simulation: Simulation.AUCUN

        self.temps_de_sortie = []
        self.temps_maximal = temps_maximal

        constructeur_simulation = ConstructeurSimulation(configuration_simulation, self.ajouterTempsSortie)
        self.simulation = constructeur_simulation.simulation

        self.action_mise_a_jour_secondaire = action_mise_a_jour_secondaire
        self.simulation.action_mise_a_jour = self.actionMiseAJour

    def lancer(self):
        self.simulation.lancer()

    def ajouterTempsSortie(self, temps):
        self.temps_de_sortie.append(temps)

    def actionMiseAJour(self, simulation):
        commandes = self.action_mise_a_jour_secondaire(simulation)
        if simulation.temps_depuis_lancement > self.temps_maximal:
            commandes = commandes | Simulation.ARRET
        return commandes
        

##
class TraitementDeDonnees(object):
    
    
    def __init__(self, donnees_test):
        
        self.donnees_test = donnees_test
        
        
    
    
    def pourcentage_cumule_croissant(self):
        pourcentages = [k/len(self.donnees_test) for k in range (len(self.donnees_test))]
        return pourcentages
        
        
    def tracer_pourcentage(self):
        abscisse = self.donnees_test
        ordonnee = self.pourcentage_cumule_croissant()
        return plot(abscisse, ordonnee)
        
##
    def tracer(self):
        pass
