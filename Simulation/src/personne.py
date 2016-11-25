from pymunk.vec2d import Vec2d
import math
import pymunk

class Personne(object):

    RAYON = 5
    MASSE = 70
    MOMENT = pymunk.moment_for_circle(MASSE, 0, RAYON)
    FORCE_DEPLACEMENT = 5 * 10**4
    VITESSE_MAXIMALE = 50
    COEFFICIENT_TEST = 1.5


    def __init__(self, position, lieu_ferme):
        self.body = pymunk.Body(Personne.MASSE, Personne.MOMENT)
        self.shape = pymunk.Circle(self.body, Personne.RAYON)
        self.body.position = position
        
        self.lieu_ferme = lieu_ferme

    def estSortie(self):
        return self.body.position.y < self.lieu_ferme.avoirCentrePorte().y

    def ajouterDansEspace(self, espace):
        espace.add(self.body, self.shape)

    def traiterVitesse(self):
        if self.body.velocity.length > Personne.VITESSE_MAXIMALE:
            self.body.velocity *= Personne.VITESSE_MAXIMALE / self.body.velocity.length

    def update(self):
        self.traiterVitesse()
        if not self.estSortie():
            test_direction = TestProximite(self.body.position, self.lieu_ferme, Personne.COEFFICIENT_TEST * Personne.RAYON)
            point_direction = test_direction.avoirPointPlusProcheSortie()
            force = (point_direction - self.body.position).normalized() * Personne.FORCE_DEPLACEMENT
            self.body.apply_force_at_local_point(force, Vec2d(0, 0))


class TestProximite(object):

    ENSEMBLE_BASE_POINT_TEST = [ Vec2d(math.cos(2 * math.pi * i / 8), math.sin(2 * math.pi * i / 8)) for i in range(8) ]
    NOMBRE_POINT = 8

    def __init__(self, position, lieu_ferme, rayon):
        self.position = position
        self.lieu_ferme = lieu_ferme
        self.ensemble_point = [ rayon * point + self.position for point in TestProximite.ENSEMBLE_BASE_POINT_TEST ]

        self.retirerPointDansObstacle()

    def retirerPointDansObstacle(self):
        point_dans_obstacle = [ False ] * TestProximite.NOMBRE_POINT
        for index_point in range(TestProximite.NOMBRE_POINT):
            for obstacle in self.lieu_ferme.ensemble_obstacle:
                if obstacle.pointEstAInterieur(self.ensemble_point[index_point]):
                    point_dans_obstacle[index_point] = True
        self.ensemble_point = [ self.ensemble_point[i] for i in range(TestProximite.NOMBRE_POINT) if not point_dans_obstacle[i] ]

    def avoirPointPlusProcheSortie(self):
        if self.ensemble_point == []:
            return None
        point_plus_proche = self.ensemble_point[0]
        distance_plus_proche = point_plus_proche.get_distance(self.lieu_ferme.avoirCentrePorte())
        for point in self.ensemble_point[1:]:
            distance_courante = point.get_distance(self.lieu_ferme.avoirCentrePorte())
            if distance_courante < distance_plus_proche:
                point_plus_proche = point
                distance_plus_proche = distance_courante
        return point_plus_proche
