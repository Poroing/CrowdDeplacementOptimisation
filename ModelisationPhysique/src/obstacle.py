from pymunk.vec2d import Vec2d
from representation_categories import RepresentationCategorie
from representation import Representation, Rectangle, Cercle, Polygon, Segment
import pymunk
import geometrie

class Obstacle(Representation):
    '''Keyword Arguments: position'''

    def __init__(self, **kwargs):
        kwargs['corps'] = pymunk.Body(body_type=pymunk.Body.STATIC)
        super().__init__(**kwargs)

        self.filter = pymunk.ShapeFilter(
            categories=RepresentationCategorie.OBSTACLE.value)

    def peutEtrePasserEntre(self, rayon, autre):
        for autre_sommet in autre.sommets:
            for sommet in self.sommets:
                if autre_sommet.get_distance(sommet) < rayon:
                    return False

        for sommet in self.sommets:
            for arete in autre.genererAretes():
                projection = geometrie.avoirProjectionSurSegment(sommet, arete)
                if projection is None:
                    continue
                distance_arrete = sommet.get_distance(projection)
                if distance_arrete < rayon:
                    return False

        for sommet in autre.sommets:
            for arete in self.genererAretes():
                projection = geometrie.avoirProjectionSurSegment(sommet, arete)
                if projection is None:
                    continue
                distance_arrete = sommet.get_distance(projection)
                if distance_arrete < rayon:
                    return False

        return True

class OsbtacleSegment(Obstacle, Segment):
    '''Keywords Arguments: position, point1, point2'''
    pass
    

class ObstaclePolygonale(Obstacle, Polygon):
    '''Keywords Arguments: position, sommets'''
    pass


class ObstacleRectangulaire(ObstaclePolygonale, Rectangle):
    '''Keywords Arguments: position, hauteur, largeur'''

    def pointEstAInterieur(self, point):
        return ( point.x > self.position.x and point.x < self.position.x + self.largeur
            and point.y > self.position.y and point.y < self.position.y + self.hauteur)


#Cette objet n'est pas utiliser mais pourrais être à l'avenir
#Il devra être modifié dns ce cas
class ObstacleCirculaire(Obstacle, Cercle):
    '''Keyword Arguments: position, rayon'''

    def pointEstAInterieur(self, point):
        return self.position.get_distance(point) < self.rayon
