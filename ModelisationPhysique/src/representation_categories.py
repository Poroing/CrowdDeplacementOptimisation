from enum import Enum

class RepresentationCategorie(Enum):

    PERSONNE = 0x1
    OBSTACLE = 0x2

def avoirMasqueSansValeur(masque, valeur):
    return masque ^ valeur
