## TIPE Foule

from random import *
from copy import *



def MeilleurBatiment( batiment):
    """ Cette fonction prend un batiment et en produit des variantes pour chercher le batiment le plus efficace"""
    
    #On va dans un premier temps établir une liste des liaisons mutables
    def listeMutables( batiment):
        """ listeMutables crée une liste des liaisons mutables entre salles""" 
        
        #Pour trouver cela on va utiliser la fonction de map de graphe 
        def liaisons( salle):
            return [(salle,k[0],k[1]) for k in salle.sallesAdjacentes if k[1]==CHEMIN_BLOQUE or k[1]==CHEMIN_RENTRANT_MUTABLE]
        #liaisons est de la forme [(salle1,salle2,sens1->2)]
        sortie = mapGraphe( batiment.sorties[0], liaisons)
        return (sortie,batiment.efficacite())
        
    #Ensuite on a une fonction pour créer des batiments variant et une pour les vérifier
    def variationsBatiment( batiment, n):
        """variation crée n variantes du batiment"""
        
        liaisons,efficacite = listeMutables(batiment)
        variations = [liaisons]
        for k in range(n):
            variante = liaisons.copy()
            for i in randint(1,len(liaisons)):
                for j in generateurListeAleat(i):
                    variante[j]=randint(-1,1)
            variations.append(variante)
        return variations
    
            
            
            
            
            
        
        
            
        
    
    
    





    
         
