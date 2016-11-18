from pymunk.vec2d import Vec2d
import pymunk


class ObstacleRectangulaire (object):
    def __init__ (self, hauteur, largeur, position):
        self.hauteur = hauteur
        self.largeur = largeur
        self.position = position
        
    def aujouterDansEspace(self, espace):
        
        sommet_bas_gauche = self.position
        sommet_bas_droit = self.position + Vec2d(self.largeur, 0)
        sommet_haut_droit = self.position + Vec2d(self.largeur, self.hauteur)
        sommet_haut_gauche = self.position + Vec2d(0, self.hauteur)
        
        corps_mur_haut = pymunk.Body(body_type=pymunk.Body.STATIC)
        mur_haut = pymunk.Segment(corps_mur_haut, sommet_haut_gauche, sommet_haut_droit, 0.0)
        espace.add(corps_mur_haut, mur_haut)

        corps_mur_gauche = pymunk.Body(body_type=pymunk.Body.STATIC)
        mur_gauche = pymunk.Segment(corps_mur_gauche, sommet_haut_gauche, sommet_bas_gauche, 0.0)
        espace.add(corps_mur_gauche, mur_gauche)

        corps_mur_droit = pymunk.Body(body_type=pymunk.Body.STATIC)
        mur_droit = pymunk.Segment(corps_mur_droit, sommet_bas_droit, sommet_haut_droit, 0.0)
        espace.add(corps_mur_droit, mur_droit)

        corps_mur_bas = pymunk.Body(body_type=pymunk.Body.STATIC)
        mur_bas = pymunk.Segment(corps_mur_ba, sommet_bas_gauche, sommet_bas_droit, 0.0)
        espace.add(corps_mur_bas, mur_bas)
        
        
        