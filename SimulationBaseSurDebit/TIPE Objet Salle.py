## Objet Salle

class Salle ( object) :
    
    """Une salle a : -un nombre total de personnes nombrePersonnes
                     -un nombre maximal de personnes nombrePersonnesMaximumimal
                     -une liste des salles adjacentes et leur orientation
                     -une liste des débits de sortie pour les salles suivantes
                     -un indice aEteVisite qui determine si il a été visité ce tour
                     -un booleen estSortie qui indique si c'est une sortie
                     
        nomenclature pour l'ordre :    salle précédente
                                             |
                                       salle actuelle
                                             |
                                       salle suivante
                                             |
                                            ...
                                             |
                                           sortie
    """
                     
    CHEMIN_RENTRANT_FIXE = -2
    CHEMIN_RENTRANT_MUTABLE = -1
    CHEMIN_BLOQUE = 0
    CHEMIN_SORTANT_MUTABLE = 1
    CHEMIN_SORTANT_FIXE = 2
    INFINI = 10**100
    
    def __init__( self, nombrePersonnes, nombrePersonnesMaximum, nom='Salle', sortie=False):
        """ Construit une salle avec les paramètres donnés
        
            salle( nombrePersonnes, nombrePersonnesMaximum,  nom='Salle', sortie=False)
        
            nombrePersonnes = int
            nombrePersonnesMaximum = int
            sortie = booleen
            nom = string                                                            """
        
        self.nombrePersonnes = nombrePersonnes                  # int
        self.nombrePersonnesMaximum = nombrePersonnesMaximum    # int       
        self.sallesAdjacentes = []                              # list( ( salles, int)) decris les salles et leurs orientations
        self.debitsSortie = []                                  # list( int)
        self.aEteVisite = False                                 # bool
        self.estSortie = sortie                                 # bool
        self.nom = nom                                          # string
        
        
    def ajouterAdjacent( self, salleAdjacente, orientationAreteSalles, debitSortie=1):
        """Ajoute une salle adjacente à celle ci et de même sur l'autre"""
        #On modifie la liste d'adjacence pour la salle actuelle
        self.sallesAdjacentes.append((salleAdjacente,orientationAreteSalles))      
        self.debitsSortie.append(debitSortie)
        #On modifie la liste d'adjacence pour la salle mise en adjacence
        salleAdjacente.sallesAdjacentes.append((self,-orientationAreteSalles)) 
        salleAdjacente.debitsSortie.append(debitSortie)
        
    def enleverAdjacent( self, salleAdjacente):
        """Enlève une salle des salles adjacentes"""
        self.sallesAdjacentes.remove(salleAdjacentes)
        salleAdjacente.sallesAdjacentes.remove(self)
        
        
    def sortieConnexe( self):
        """ renvoie toutes les sorties connexes"""
        self.aEteVisite = True
        sortie = []
        #On va parcourir le graphe recursivement et on explicite les cas de modification de la liste (bool : la salle est une sortie)
        if self.estSortie :
            sortie.append(self)
        #Pour chacun des salles adjacentes (lien non nul entre les salles) on réapplique la récursion
        for k in range(len(self.sallesAdjacentes)) :
            if not self.sallesAdjacentes[k][0].aEteVisite and self.sallesAdjacentes[k][1]!=0 :
                sortie.extend(self.sallesAdjacentes[k][0].sortieConnexe())
        self.aEteVisite = False
        return sortie        
        
        
    def etatSuivant( self):
        """Fais passer la salle au tour suivant"""
        #On a une liste des salles parentes de celle là et leur debit de sortie
        sallesPrecedentes = [k[0] for k in self.sallesAdjacentes if k[1]<0]
        debitSallesPrecedentes = [k[1] for k in self.sallesAdjacentes if k[1]<0]
        #Pour chacune des salles parentes (ordre aléatoire) on fait passer dans la salle le nombre de personnes minimal entre le debit max,
        #le nombre de places libres et le nombre de personnes restantes dans la salle adjacente
        for index in generateurListeAleat(len(sallesPrecedentes)):
            if self.nombrePersonnes<self.nombrePersonnesMaximum:
                depl = min( abs(debitSallesPrecedentes[index]), sallesPrecedentes[index].nombrePersonnes,self.nombrePersonnesMaximum-self.nombrePersonnes)
                self.nombrePersonnes+=depl
                sallesPrecedentes[index].nombrePersonnes-=depl


    def __repr__(self):
        """Sert à représenter la salle (fonction pour les tests et le débogage)"""
        retour = " \n \n"+self.nom + " : \nCette salle peut contenir "+str(self.nombrePersonnesMaximum)+" personnes \n"
        retour += "Elle en contiens actuellement " + str(self.nombrePersonnes) + " personnes \n"
        if self.estSortie :
            retour += "Est une sortie"
        else :
            retour += "N'est pas une sortie"
        return retour
        
        
        


    
        
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    