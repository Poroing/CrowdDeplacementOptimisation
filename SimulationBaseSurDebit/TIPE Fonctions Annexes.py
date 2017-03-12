## Fonctions Annexes

from random import *

def generateurListeAleat( n):
    """ Génère les n nombres entre 1 et n dans un ordre aléatoire"""
    A=[]
    while len(A) <n:
        a = randint(0,n-1)
        if a not in A :
            A.append(a)
    for k in A:
        yield k
    
def boolFunOnList( boolFun, liste):
    for k in liste:
        if not boolFun(k):
            return False
    return True        
    
## Fonction Annexe sur les Graphes

def mapGraphe( Noeud, fonction,parcouru=None,retour=None):
    """ mapGraphe va parcourir le graphe et appliquer la fonction sur chaque noeud et renvoyer la liste des resultats"""
    # on vérifie le cas par défaut sans mettre [] dans les paramètres pour eviter
    # les problèmes dus à la globalité des listes
    if parcouru is None :
        parcouru=[]
    if retour is None :
        retour=[]
    parcouru.append(Noeud)
    retour.append(fonction(Noeud))
    for k in Noeud.sallesAdjacentes :
        x=k[0]
        if x not in parcouru:
            mapGraphe(x,fonction,parcouru,retour)
    return retour

## Fonctions Annexes pour travailler sur des listes de listes (Union,Intersection,Presence)

def unionList(liste):
    """ renvoie une union des listes de la liste"""
    sortie = []
    for k in liste :
        for i in k :
            if i not in sortie :
                sortie.append(i)
    return sortie
    
def interList(liste):
    """ renvoie une intersction des listes de la liste"""
    sortie = liste[0]
    mem = []
    for k in liste :
        for i in k :
            if i in sortie :
                mem.append(i)
        sortie = mem.copy()
        mem = []
    return sortie
    
def presenceElementListe(element,liste):
    """ renvoie si l'element est dans une des listes de liste"""
    for k in liste :
        for i in k :
            if element==i :
                return True
    return False
            
        
    
    
    
    
    
    
    
    
    
    
    
    
    
            