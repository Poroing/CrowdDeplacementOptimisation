## TIPE

from collections import deque
from random import *

#pour les files on utilise decque

class salle ( object) :
    
    # Une salle a : -un nombre de personnes maximal
    #               -une liste d'attente pour entre dans la salle
    #               -une liste des salles precedentes (origines)
    #               -une liste des salles suivantes 
    #               -une liste des débits de sortie pour les salles suivantes
    #               -un indice de visite qui determine si il a été visité ce tour
    #               -si c'est une sortie
    
    def __init__( self, nb, mx, ori, srt=False):
        
        self.nombre = nb
        
        self.max = mx
         
        self.origines = ori
        
        self.attente = deque()
        
        self.suivants = []
        
        self.debits = []
        
        self.visite = False
        
        self.estSortie = srt
        
    def ajouterSuivant( self, suiv, deb):
        
        self.suivants.append(suiv)
        
        self.debits.append(suiv)
        
        
    def etatSuivant( self):
        
        if self.attente != deque() :
            while  self.nombre<self.max-self.attente[0] :
            
                self.nombre += self.attente.popleft()
            
        if self.nombre<self.max and self.attente != deque():
            
            self.attente[0]=self.attente[0]- (self.max - self.nombre)
            self.nombre = self.max
            
        
        if self.suivants == None :
            
            self.nombre -= self.debits
            
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
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
        
        
