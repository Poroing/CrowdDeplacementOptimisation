from pymunk.vec2d import Vec2d
import math
import functools

class TestBordsObstacle(object):

    def __init__(self, position, espace, rayon, position_voulue):
        self.espace = espace
        self.rayon = rayon
        self.point_a_suivre = None
        self.position_voulue = position_voulue
        self.update(position)

    def sommetEstAccessible(self, sommet):
        return not self.espace.cercleEstEnDehorsDeLieuFerme(sommet, self.rayon * 2)

    #def avoirSommets

    def update(self, position):
        info_lancer_rayon = self.espace.avoirInfoSurLancerRayon(position,
            self.position_voulue)

        if info_lancer_rayon is None:
            self.point_a_suivre = self.position_voulue
        else:
            avoirDistanceAPointRayon = lambda sommet: sommet.get_distance(info_lancer_rayon.point)
            transformerEnCoordoneeGlobal = lambda sommet: info_lancer_rayon.shape.body.local_to_world(sommet)
            sommets = list(map(transformerEnCoordoneeGlobal, info_lancer_rayon.shape.get_vertices()))
            sommets_accessible = filter(self.sommetEstAccessible, sommets)
            self.point_a_suivre = min(sommets_accessible, key=avoirDistanceAPointRayon, default=sommets[0])

class TestProximite(object):

    COEFFICIENT_TEST = 3

    def __init__(self, position, espace, rayon, position_voulue, nombre_point=16):
        self.espace = espace
        self.nombre_point = nombre_point
        self.position_voulue = position_voulue
        self.position = position
        self.ensemble_point = list(
            self.genererEnsemblePoint(rayon * TestProximite.COEFFICIENT_TEST))
        self.point_a_suivre = self.ensemble_point[0]

    def genererEnsemblePoint(self, rayon):
        for i in range(self.nombre_point):
            point_local_x = math.cos(2 * math.pi * i / self.nombre_point)
            point_local_y = math.sin(2 * math.pi * i / self.nombre_point)
            point_local = rayon * Vec2d(point_local_x, point_local_y)
            yield self.position + point_local
            

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
            key=lambda p: p.get_distance(self.position_voulue),
            default=self.ensemble_point[0])
