from pymunk.vec2d import Vec2d
import pymunk

class ObstacleRectangulaire (object):

    def __init__ (self, hauteur, largeur, position):

        self.corps = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.corps.position = position + Vec2d(largeur * 1/2, hauteur * 1/2)

        self.representation = pymunk.Poly.create_box(self.corps, size=(largeur, hauteur))
        
    def ajouterDansEspace(self, espace):
        espace.add(self.corps, self.representation)
