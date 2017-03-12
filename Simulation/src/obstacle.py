from pymunk.vec2d import Vec2d
from representation_categories import RepresentationCategorie
from representation import Representation, Rectangle, Cercle
import pymunk

class Obstacle(Representation):
    '''Keyword Arguments: position'''

    def __init__(self, **kwargs):
        kwargs['corps'] = pymunk.Body(body_type=pymunk.Body.STATIC)
        super().__init__(**kwargs)

        self.filter = pymunk.ShapeFilter(
            categories=RepresentationCategorie.OBSTACLE.value)

class ObstacleRectangulaire(Obstacle, Rectangle):
    '''Keywords Arguments: position, hauteur, largeur'''

    def __init__ (self, **kwargs):
        super().__init__(**kwargs)

    def pointEstAInterieur(self, point):
        return ( point.x > self.position.x and point.x < self.position.x + self.largeur
            and point.y > self.position.y and point.y < self.position.y + self.hauteur)


class ObstacleCirculaire(Obstacle, Cercle):
    '''Keyword Arguments: position, rayon'''
        
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def pointEstAInterieur(self, point):
        return self.positon.get_distance(point) < self.rayon
