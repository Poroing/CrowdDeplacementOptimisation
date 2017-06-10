import collections
import numpy as np
import functools
import operator

class EnsembleRappelle(object):
    '''Regroupe plusieurs rappelle et renvoie l'ensemble des resultats'''

    def __init__(self):
        self.ensemble_rappelles = []

    def ajouter(self, rappele):
        self.ensemble_rappelles.append(rappele)

    def __call__(self, *args, **kwargs):
        resultats = []
        for rappele in self.ensemble_rappelles:
            resultats.append(rappele(*args, **kwargs))
        return resultats

class EnsembleRappelleRenvoyantCommande(EnsembleRappelle):

    AUCUN = 0x0

    def __call__(self, *args, **kwargs):
        resultats = super().__call__(*args, **kwargs)
        return functools.reduce(
            operator.or_,
            resultats,
            EnsembleRappelleRenvoyantCommande.AUCUN)

class KeyPairDict(collections.UserDict):
    '''Une table de hachage avec des pair pour clefs

        A utiliser surtout dans le cas d'un petit nombre
        d'insertions et d'un grand nombre de recuperation
        de valeurs
    '''

    #Lorsque peut d'insertions sont faites on peut s'autoriser
    #de stocker toutes les permutations des clefs avec la valeur
    #associée pour ainsi éviter de devoir faire deux recherche
    #à chaque recherche d'une clefs dans la table

    def transpose(self, pair):
        element1, element2 = pair
        return element2, element1

    def __setitem__(self, key, value):
        self.data[key] = value
        self.data[self.transpose(key)] = value

    def __delitem__(self, key):
        del self.data[key]
        del self.data[self.transpose(key)]

class KeyIterableDict(collections.UserDict):
    '''Dictionaire pouvant avoir n'importe quelle iterable comme clefs

        deux iterable a, b sont considérées comme égaux lorsque
        all(v == w for v, w in zip(a, b))

    '''

    #tuple est le seul type iterable qui est hachable est vérifie
    #all(v == w for v, w in zip(a, b)) => hash(a) == hash(b)
    #pour avoir la propriété recherché on convertie toutes les clefs
    #en tuple

    def avoirTuple(self, iterable):
        if isinstance(iterable, collections.Iterable):
            return tuple(map(self.avoirTuple, iterable))
        return iterable

    def __contains__(self, key):
        return self.avoirTuple(key) in self.data

    def __setitem__(self, key, value):
        self.data[self.avoirTuple(key)] = value

    def __getitem__(self, key):
        return self.data[self.avoirTuple(key)]

    def __delitem__(self, key):
        del self.data[self.avoirTuple(key)]

class EmptyListDict(collections.UserDict):
    '''Dictionnaire associant une liste vide à tout clefs non présente'''

    def __getitem__(self, key):
        return self.data.setdefault(key, [])

def creerListeDoubleDimension(hauteur, largeur, valeur_defaut=None):
    return [ [ valeur_defaut for _ in range(largeur) ] for _ in range(hauteur) ]

class Case(object):

    @staticmethod
    def genererQuatreDirections():
        yield Case(1, 0)
        yield Case(-1, 0)
        yield Case(0, 1)
        yield Case(0, -1)

    def genererHuitDirections():
        yield Case(1, 0)
        yield Case(-1, 0)
        yield Case(0, 1)
        yield Case(0, -1)
        yield Case(1, 1)
        yield Case(-1, -1)
        yield Case(-1, 1)
        yield Case(1, -1)

    def __init__(self, ligne, colonne):
        self.ligne = ligne
        self.colonne = colonne

    def __add__(self, other):
        return Case(self.ligne + other.ligne, self.colonne + other.colonne)

    def genererCaseAdjacentes(self, directions):
        for direction in directions:
            yield direction + self

    def __repr__(self):
        return 'Case({}, {})'.format(self.ligne, self.colonne)

class TableauDeuxDimension(object):

    def __init__(self, **kwargs):
        self.nombre_lignes = kwargs['nombre_lignes']
        del kwargs['nombre_lignes']

        self.nombre_colonnes = kwargs['nombre_colonnes']
        del kwargs['nombre_colonnes']

        if 'valeur_defaut' not in kwargs:
            kwargs['valeur_defaut'] = None

        self.donnee = creerListeDoubleDimension(
            self.nombre_lignes,
            self.nombre_colonnes,
            valeur_defaut=kwargs['valeur_defaut'])
        del kwargs['valeur_defaut']
            
        super().__init__(**kwargs)

    def __getitem__(self, case):
        return self.donnee[case.ligne][case.colonne]

    def __setitem__(self, case, valeur):
        self.donnee[case.ligne][case.colonne] = valeur

    def __contains__(self, case):
        return (case.ligne >= 0
            and case.colonne >= 0
            and case.ligne < self.nombre_lignes
            and case.colonne < self.nombre_colonnes)

    def __repr__(self):
        return 'TableauDeuxDimension({}, {})'.format(
            self.nombre_lignes, self.nombre_colonnes)

    def genererValeurs(self):
        return map(self.__getitem__, self.genererCases())

    def genererCases(self):
        for ligne in range(self.nombre_lignes):
            for colonne in range(self.nombre_colonnes):
                yield Case(ligne, colonne)

def parcoursEnLargeur(debuts_et_valeurs, voisins, assigner_valeur, tableau_finale):
    '''Functions Arguments:
            voisins(case_courante, tableau_finale),
            valeur_case(case_voisise, case_courante, tableu_finale)
    '''

    deja_vue = TableauDeuxDimension(
        nombre_lignes=tableau_finale.nombre_lignes,
        nombre_colonnes=tableau_finale.nombre_colonnes,
        valeur_defaut=False)

    queue = collections.deque()

    for debut, valeur in debuts_et_valeurs:
        queue.append(debut)
        deja_vue[debut] = True
        tableau_finale[debut] = valeur

    while len(queue) > 0:
        case_courante = queue.popleft()
        #print(tableau_finale.avoirCentreCase(case_courante))
        #input()
        for case_voisine in voisins(case_courante, tableau_finale):
            if case_voisine not in tableau_finale or deja_vue[case_voisine]:
                continue
            deja_vue[case_voisine] = True
            queue.append(case_voisine)
            assigner_valeur(case_voisine, case_courante, tableau_finale)
    
def unzip(iterable):
    lefts = []
    rights = []
    for left, right in iterable:
        lefts.append(left)
        rights.append(right)
    return lefts, rights
        
def fusioner_dictionnaires(dic1, dic2):
    sortie = {}
    sortie.update(dic1)
    sortie.update(dic2)
    return sortie

def mapMatrix(function, matrix):
    return np.matrix(list(map(function, matrix.flat))).reshape(matrix.shape)
