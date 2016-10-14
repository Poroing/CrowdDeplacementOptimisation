import math

class Vecteur(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vecteur(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vecteur(self.x - other.x, self.y - other.y)

    def __mul__(self, scalaire):
        return Vecteur(self.x * scalaire, self.y * scalaire)

    def norme(self):
        return math.sqrt(self.x**2 + self.y**2)

    @staticmethod
    def distance(vecteur1, vecteur2):
        return (vecteur1 - vecteur2).norme()

    
class Sortie(object):

    def __init__(self, paroi, position, largeur):
        self.paroi
        self.position = position
        self.largeur = largeur


class Paroi(object):

    def __init__(self, extremite1, extremite2):
        self.extremite1 = extremite1
        self.extremite2 = extremite2
        self.ensemble_sorties = []

    def ajouterSortie(self, position, largeur):
        sortie = Sortie(self, position, largeur)

        if position + largeur / 2 > 1 and position - largeur / 2 < 1:
            raise ValueError('Une sortie ne peut dépasser de la paroi')

        self.ensemble_sorties.append(sortie)
        
    def initialiserLongueur(self):
        self.longueur = Vecteur.distance(self.extremite1, self.extremite2)


class LieuFerme(object):

    def __init__(self, ensemble_sommets):
    '''
        Aruments:
        ensembleSommets: ensemble des sommets consécutifs
    '''
        self.ensemble_parois = []
        for i in range(len(ensemble_sommets) - 1)
            self.paroi.append(Paroi(ensemble_sommets[i], ensemble_sommets[i + 1]))
        self.paroi.append(Paroi(ensemble_sommets[0], ensemble_sommets[-1]))
        
    
