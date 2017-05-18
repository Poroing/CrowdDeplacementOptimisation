from personne import Personne
import time
from random import randint


class Source(object):

    def __init__(self, espace, position, periode, rayon_min, rayon_max, masse_surfacique):
        self.periode = periode
        self.position = position
        self.espace = espace
        self.temps_derniere_ajout = 0
        self.rayon_max = rayon_max
        self.rayon_min = rayon_min
        self.masse_surfacique = masse_surfacique


    def mettreAJour(self, temps):
        personne = None
        if temps - self.temps_derniere_ajout > self.periode:
            
            rayon = randint(self.rayon_min, self.rayon_max)
            
            personne = Personne(self.masse_surfacique, rayon, self.position, self.espace)
            self.espace.ajouterPersonne(personne)
            self.temps_derniere_ajout = temps
        return personne
