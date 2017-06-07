from functools import partial
import matplotlib.pyplot as plt
from simulation import Simulation, ConstructeurSimulation
import math

class RecuperationDeDonnees(object):
    
    def __init__(self, configuration_simulation, arreter_apres_temps=True, temps_maximal=0,
            arreter_apres_sortie=False, action_mise_a_jour_secondaire=None):
        if action_mise_a_jour_secondaire is None:
            action_mise_a_jour_secondaire = lambda simulation: Simulation.AUCUN

        self.temps_de_sortie = []

        self.temps_maximal = temps_maximal
        self.arreter_apres_temps = arreter_apres_temps

        self.arreter_apres_sortie = arreter_apres_sortie
        self.nombre_personnes_initiales = configuration_simulation['personnes']['nombre']

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
        if (self.arreter_apres_sortie
                and self.avoirNombrePersonneSortie() >= self.nombre_personnes_initiales):
            commandes = commandes | Simulation.ARRET
            
        return commandes
        
class TraitementDeDonnees(object):
    
    
    def __init__(self, temps_sortie):
        
        self.ensemble_temps_sortie = temps_sortie
        self.rendreTempsSortieUnique() 
        self.nombre = len(self.ensemble_temps_sortie)

    def rendreTempsSortieUnique(self):
        nouveau_ensemble_temps_sortie = []
        for temps_sortie in self.ensemble_temps_sortie:
            if (nouveau_ensemble_temps_sortie != []
                    and temps_sortie == nouveau_ensemble_temps_sortie[-1]):
                continue
            nouveau_ensemble_temps_sortie.append(temps_sortie)
        self.ensemble_temps_sortie = nouveau_ensemble_temps_sortie
    
    def personnes_en_fonction_du_temps(self):
        plt.plot([0] + self.ensemble_temps_sortie, list(range(len(self.ensemble_temps_sortie)+1)))
    
    def debit_ordre_premier(self):
        derivee = [0]
        for x in range (1,self.nombre) :
            print(self.ensemble_temps_sortie[x] - self.ensemble_temps_sortie[x-1])
            derivee.append(1/(self.ensemble_temps_sortie[x] - self.ensemble_temps_sortie[x-1]))
            
        return derivee + [0]
        
    def debit_ordre_quatre(self):
        derivee = [0]
        derivee.append((1/self.ensemble_temps_sortie[1]-self.ensemble_temps_sortie[0]))
        for x in range  (2, self.nombre - 2):
            
            derivee.append(- 12/( -self.ensemble_temps_sortie[x-2] + 8 * self.ensemble_temps_sortie[x-1]
                - 8 * self.ensemble_temps_sortie[x+1] + self.ensemble_temps_sortie[x+2]))
        
        derivee.append(1/(self.ensemble_temps_sortie[self.nombre-2]-self.ensemble_temps_sortie[self.nombre-3]))
        derivee.append(1/(self.ensemble_temps_sortie[self.nombre-1]-self.ensemble_temps_sortie[self.nombre-2]))
        return derivee + [0]

    def avoirEcartTypeEtMoyenne(self, ensemble):
        moyenne = sum(ensemble) / len(ensemble)
        moyenne_carree = sum(x**2 for x in ensemble) / len(ensemble)
        return math.sqrt(moyenne_carree - moyenne**2), moyenne

    def avoirEnsembleSansValeurIninteressante(self, ensemble):
        ecart_type, moyenne= self.avoirEcartTypeEtMoyenne(ensemble)
        return [ x for x in ensemble if abs(x - moyenne) < 2 * ecart_type ]

    def avoirDebitMoyen(self, remove_irelevant_value=True):
        if self.nombre == 0:
            return 0
        ensemble_debits = self.debit_ordre_quatre()
        if remove_irelevant_value:
            ensemble_debits = (
                self.avoirEnsembleSansValeurIninteressante(ensemble_debits))

        moyenne = sum(ensemble_debits) / len(ensemble_debits)
        return moyenne
