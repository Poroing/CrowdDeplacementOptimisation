from pymunk.vec2d import Vec2d
from representation_categories import RepresentationCategorie
from representation import CercleDynamique
from test_point_suivre import TestBordsObstacle, TestProximite, TestDichotomie
import math
import pymunk
import operator
import itertools
from random import randint

class Personne(CercleDynamique):

    VITESSE_MAXIMALE = 222
    COEFFICIENT_EVITEMENT = 0.4

    def __init__(self, masse_surfacique, rayon, position, espace, test_direction_cls=TestDichotomie):
        super().__init__(masse_surfacique = masse_surfacique, rayon=rayon, position=position)
        
        
        self.force_deplacement = self.rayon * 10**4
        self.filter = pymunk.ShapeFilter(categories=RepresentationCategorie.PERSONNE.value)
        self.espace = espace
        self.test_direction = test_direction_cls(
            position=position,
            espace=espace,
            rayon=self.rayon,
            position_voulue=self.sortieLaPlusProche())
        
    
    def sortieLaPlusProche(self):
        position = self.position
        liste_centres = self.espace.lieu_ferme.avoirCentrePortes()
        distmin = position.get_distance(liste_centres[0])
        centre_min = liste_centres[0]
        
        for centre in (liste_centres):
            dist = position.get_distance(centre)
            if dist < distmin :
                distmin, centre_min = dist, centre
                
        return centre_min
    
    def pointEstAInterieur(self, point):
        return point.get_distance(self.body.position) < self.rayon

    def personneEstTropProche(self, personne):    
        return (personne.body.position.get_distance(self.body.position)
            < (2 + Personne.COEFFICIENT_EVITEMENT) * self.rayon)

    def estTropProcheDePersonne(self):
        return any(map(lambda personne: self.personneEstTropProche(personne),
            self.espace.ensemble_personnes))

    def estSortie(self):
        return self.espace.lieu_ferme.pointEstAExterieur(self.position)

    def traiterVitesse(self):
        if self.corps.velocity.length > Personne.VITESSE_MAXIMALE:
            self.corps.velocity *= Personne.VITESSE_MAXIMALE / self.body.velocity.length

    def update(self):
        self.traiterVitesse()
        if not self.estSortie():
            self.test_direction.update(self.body.position)
            force = (self.test_direction.point_a_suivre - self.body.position).normalized() * self.force_deplacement
            self.body.apply_force_at_local_point(force, Vec2d(0, 0))
