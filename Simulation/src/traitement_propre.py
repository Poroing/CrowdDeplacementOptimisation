
from matplotlib.pyplot import plot

    
##


class RecuperationDeDonnees(object):
    
    def __init__(self, configuration_simulation):
        
        
        self.temps_de_sortie = []
        self.simulation = simulation(configuration_simulation, self.ajouterTempsSortie)
        
        
        
    def ajouterTempsSortie(self, temps):
        self.temps_de_sortie.append(temps)


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
    def tracer