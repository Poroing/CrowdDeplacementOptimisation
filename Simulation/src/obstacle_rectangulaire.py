from pymunk.vec2d import Vec2d
from representation_categories import RepresentationCategorie
import pymunk

class ObstacleRectangulaire (object):

    def __init__ (self, hauteur, largeur, position):
        self.largeur = largeur
        self.hauteur = hauteur
        self.position = Vec2d(position)

        self.corps = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.corps.position = position + Vec2d(largeur * 1/2, hauteur * 1/2)

        self.representation = pymunk.Poly.create_box(self.corps, size=(largeur, hauteur))
        self.representation.filter = pymunk.ShapeFilter(categories=RepresentationCategorie.OBSTACLE.value)

    def pointEstAInterieur(self, point):
        return ( point.x > self.position.x and point.x < self.position.x + self.largeur
            and point.y > self.position.y and point.y < self.position.y + self.hauteur)
