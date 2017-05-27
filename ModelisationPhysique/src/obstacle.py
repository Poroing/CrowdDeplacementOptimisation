from pymunk.vec2d import Vec2d
from representation_categories import RepresentationCategorie
from representation import Representation, Rectangle, Cercle, Polygon, Segment
import pymunk
import geometrie
import collections

class Obstacle(Representation):
    '''Keyword Arguments: position'''

    def __init__(self, **kwargs):
        kwargs['corps'] = pymunk.Body(body_type=pymunk.Body.STATIC)
        super().__init__(**kwargs)

        self.filter = pymunk.ShapeFilter(
            categories=RepresentationCategorie.OBSTACLE.value)


class OsbtacleSegment(Obstacle, Segment):
    '''Keywords Arguments: position, point1, point2'''

    def __repr__(self):
        return 'ObstacleSegment({}, {})'.format(self.point1, self.point2)

    

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
