from pymunk.vec2d import Vec2d
import pymunk

class LieuFerme(object):

    def __init__(self, largeur=400, hauteur=800, position=(0, 0), position_porte = 0.5, largeur_porte = 85):
        self.largeur = largeur
        self.hauteur = hauteur
        self.position = Vec2d(position)
        self.largeur_porte = largeur_porte
        self.position_porte = position_porte

        if obstacle is None:
            obstacle = []
        self.ensemble_obstacle = obstacle

    def avoirCentrePorte(self):
        return self.position + Vec2d(self.largeur * self.position_porte, 0)

    def ajouterDansEspace(self, espace):
        sommet_bas_gauche = self.position
        sommet_bas_droit = self.position + Vec2d(self.largeur, 0)
        sommet_haut_gauche = self.position + Vec2d(0, self.hauteur)
        sommet_haut_droit = self.position + Vec2d(self.largeur, self.hauteur)
        sommet_porte_gauche = self.position + Vec2d(self.largeur * self.position_porte - self.largeur_porte / 2, 0)
        sommet_porte_droit = self.position + Vec2d(self.largeur * self.position_porte + self.largeur_porte /2, 0)


        corps_mur_haut = pymunk.Body(body_type=pymunk.Body.STATIC)
        mur_haut = pymunk.Segment(corps_mur_haut, sommet_haut_gauche, sommet_haut_droit, 0.0)
        espace.add(corps_mur_haut, mur_haut)

        corps_mur_gauche = pymunk.Body(body_type=pymunk.Body.STATIC)
        mur_gauche = pymunk.Segment(corps_mur_gauche, sommet_haut_gauche, sommet_bas_gauche, 0.0)
        espace.add(corps_mur_gauche, mur_gauche)

        corps_mur_droit = pymunk.Body(body_type=pymunk.Body.STATIC)
        mur_droit = pymunk.Segment(corps_mur_droit, sommet_bas_droit, sommet_haut_droit, 0.0)
        espace.add(corps_mur_droit, mur_droit)

        corps_mur_bas_droit = pymunk.Body(body_type=pymunk.Body.STATIC)
        mur_bas_droit = pymunk.Segment(corps_mur_bas_droit, sommet_bas_droit, sommet_porte_droit, 0.0)
        espace.add(corps_mur_bas_droit, mur_bas_droit)

        corps_mur_bas_gauche = pymunk.Body(body_type=pymunk.Body.STATIC)
        mur_bas_gauche = pymunk.Segment(corps_mur_bas_gauche ,sommet_bas_gauche, sommet_porte_gauche, 0.0)
        espace.add(corps_mur_bas_gauche, mur_bas_gauche)

        for obstacle in self.ensemble_obstacle:
            obstacle.ajouterDansEspace(espace)

