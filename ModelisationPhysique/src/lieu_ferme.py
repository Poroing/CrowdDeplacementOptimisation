from pymunk.vec2d import Vec2d
import pymunk

class LieuFerme(object):

    def __init__(self, largeur=400, hauteur=800, position=(0, 0), position_porte = 0.5, largeur_porte = 85):
        self.largeur = largeur
        self.hauteur = hauteur
        self.position = Vec2d(position)
        self.largeur_porte = largeur_porte
        self.position_porte = position_porte

    def avoirCentrePorte(self):
        return self.position + Vec2d(self.largeur * self.position_porte, 0)

    def pointEstAExterieur(self, point):
        return ( point.x > self.position.x + self.largeur or point.x < self.position.x
            or point.y > self.position.y + self.hauteur or point.y < self.position.y)


