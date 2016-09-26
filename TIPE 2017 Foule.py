## TIPE

from collections import deque
from random import *

#pour les files on utilise decque

class salle ( object) :
    
    """Une salle a : -un nombre de personnes maximal
                     -une liste d'attente pour entre dans la salle
                     -une liste des salles precedentes (origines)
                     -une liste des salles suivantes 
                     -une liste des débits de sortie pour les salles suivantes
                     -un indice de visite qui determine si il a été visité ce tour
                     -si c'est une sortie"""
    
    def __init__( self, nb, mx, ori, srt=False):
        """ Construit une salle avec les paramètres donnés"""
        
        self.nombre = nb # int
        self.max = mx # int
        #attente stocke les salles qui attendent à rentrer dans cette salle
        self.attente = deque() # deque((salles,int))        
        #suivants stocke les salles adjacentes 
        self.suivants = [] # liste(salles)
        #sens stocke True pour un chemin sortant et False pour un chemin rentrant
        self.sens = [] # liste(bool)
        #debits stocke le nombre de personnes qui sortent de cette salle par tour
        self.debits = [] # list(int)
        #visite stocke si ce noeud a été visité ce tour
        self.visite = False # bool
        self.estSortie = srt # bool
        
    def ajouterSuivant( self, suiv, sens, deb):
        """Ajoute une salle adjacente à celle ci"""
        self.suivants.append(suiv) 
        self.sens.append(sens)        
        self.debits.append(deb)
        
        
    def etatSuivant( self):
        """Fais passer le graphe au tour suivant"""
        
        if len(self.attente)!=0  :
            while  self.nombre<self.max-self.attente[1] :
                self.nombre += self.attente.popleft()
                
        if self.nombre<self.max and len(self.attente) != 0:
            self.attente[0]=self.attente[0]- (self.max - self.nombre)
            self.nombre = self.max
        
            
        
        if self.estSortie :
            
            self.nombre -= self.debits[0]
            
        else :
            
            a = listeAleat( len( self.suivants))
            
            for k in a :
                
                if self.nombre>0 :
                    
                    y = min(self.nombre, self.debits[k])
                    
                    self.suivants[k].attente.append(y)
                    self.nombre -= y
                    
        
                    
            
            
        
    
        
        
def listeAleat( n):
    
    A=[]
    while len(A) <n:
        a = randint(0,n-1)
        if a not in A :
            A.append(a)
    return A
            
            
            


def Evolution( salle):
    
    return 0
    
    
    
    
    
    


def TrouverRacine( salle):
    
    if salle.estSortie :
        return salle
        
    return TrouverRacine(salle.suivants[0])
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
        
        
