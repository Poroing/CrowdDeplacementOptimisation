from pymunk.vec2d import Vec2d
import math
import pymunk
import operator
import itertools

class Personne(object):

    RAYON = 21
    MASSE = 70
    MOMENT = pymunk.moment_for_circle(MASSE, 0, RAYON)
    COEFFICIENT_TEST = 3
    FORCE_DEPLACEMENT = RAYON * 10**4
    VITESSE_MAXIMALE = 222
    COEFFICIENT_EVITEMENT = 0.4

    def __init__(self, position, espace):
        self.body = pymunk.Body(Personne.MASSE, Personne.MOMENT)
        self.shape = pymunk.Circle(self.body, Personne.RAYON)
        self.body.position = position
        self.test_direction = TestProximite(position, espace, Personne.COEFFICIENT_TEST * Personne.RAYON)
        
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

class TestBordsObstacle(object):

    def __init__(self, position, espace, rayon):
        self.espace = espace
        self.point_a_suivre = None

    def update(self, positon):
        pass

class TestProximite(object):

    def __init__(self, position, espace, rayon, nombre_point=16):
        self.espace = espace
        self.nombre_point = nombre_point
        self.position = position
        self.ensemble_point = [ self.position + rayon * Vec2d(math.cos(2 * math.pi * i / self.nombre_point), math.sin(2 * math.pi * i / self.nombre_point)) for i in range(self.nombre_point) ]
        self.point_a_suivre = self.ensemble_point[0]

    def update(self, position):
        self.updatePosition(position)
        if self.espace.pointEstDansObstacle(self.point_a_suivre):
            self.updatePointASuivre()

    def forceUpdate(self, position):
        self.updatePosition(position)
        self.updatePointASuivre()
        
    def updatePosition(self, position):
        for point in self.ensemble_point:
            point += position - self.position
        self.position = position

    def updatePointASuivre(self):
            self.point_a_suivre = self.avoirPointLibrePlusProcheSortie()
            
    def genererPointsLibres(self):
        return filter(lambda point: not self.espace.pointEstDansObstacle(point), self.ensemble_point)

    def avoirPointLibrePlusProcheSortie(self):
        return min(self.genererPointsLibres(),
            key=lambda p: p.get_distance(self.espace.lieu_ferme.avoirCentrePorte()),
            default=self.ensemble_point[0])
