from pymunk.vec2d import Vec2d
from representation_categories import RepresentationCategorie
from test_point_suivre import TestBordsObstacle, TestProximite
import math
import pymunk
import operator
import itertools

class Personne(object):

    RAYON = 21
    MASSE = 70
    MOMENT = pymunk.moment_for_circle(MASSE, 0, RAYON)
    FORCE_DEPLACEMENT = RAYON * 10**4
    VITESSE_MAXIMALE = 222
    COEFFICIENT_EVITEMENT = 0.4

    def __init__(self, position, espace, test_direction_cls=TestBordsObstacle):
        self.body = pymunk.Body(Personne.MASSE, Personne.MOMENT)
        self.shape = pymunk.Circle(self.body, Personne.RAYON)
        self.shape.filter = pymunk.ShapeFilter(categories=RepresentationCategorie.PERSONNE.value)
        self.body.position = position
        self.test_direction = test_direction_cls(position, espace, Personne.RAYON,
            espace.lieu_ferme.avoirCentrePorte())
        
        self.espace = espace

    def pointEstAInterieur(self, point):
        return point.get_distance(self.body.position) < Personne.RAYON

    def personneEstTropProche(self, personne):    
        return (personne.body.position.get_distance(self.body.position)
            < (2 + Personne.COEFFICIENT_EVITEMENT) * Personne.RAYON)

    def estTropProcheDePersonne(self):
        return any(map(lambda personne: self.personneEstTropProche(personne),
            self.espace.ensemble_personnes))

    def estSortie(self):
        return self.body.position.y < self.espace.lieu_ferme.avoirCentrePorte().y

    def traiterVitesse(self):
        if self.body.velocity.length > Personne.VITESSE_MAXIMALE:
            self.body.velocity *= Personne.VITESSE_MAXIMALE / self.body.velocity.length

    def update(self):
        self.traiterVitesse()
        if not self.estSortie():
            self.test_direction.update(self.body.position)
            force = (self.test_direction.point_a_suivre - self.body.position).normalized() * Personne.FORCE_DEPLACEMENT
            self.body.apply_force_at_local_point(force, Vec2d(0, 0))
