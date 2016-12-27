import pymunk
from obstacle_rectangulaire import ObstacleRectangulaire
from personne import Personne
from pymunk.vec2d import Vec2d

class Espace(object):

    def __init__(self):
        self.pymunk_espace = pymunk.Space()

        self.lieu_ferme = None
        self.ensemble_obstacle = []
        self.ensemble_personnes = []

    def avancer(self, delta):
        self.pymunk_espace.step(delta)
        
        for personne in self.ensemble_personnes:
            personne.update()

    def pointEstDansObstacle(self, point):
        return (self.lieu_ferme.pointEstAExterieur(point)
            or any(map(lambda obstacle: obstacle.pointEstAInterieur(point),
                self.ensemble_obstacle))
            or any(map(lambda obstacle: obstacle.pointEstAInterieur(point),
                self.ensemble_personnes)))

    def ajouterElement(self, element):
        if isinstance(element, Personne):
            self.ajouterPersonne(element)
        elif isinstance(element, ObstacleRectangulaire):
            self.ajouterObstacle(element)
        else:
            raise ValueError('{} n\'est pas valide comme element d\'Espace'.format(type(element)))

    def ajouterPersonne(self, personne):
        self.ensemble_personnes.append(personne)
        self.pymunk_espace.add(personne.body, personne.shape)

    def ajouterObstacle(self, obstacle):
        self.ensemble_obstacle.append(obstacle)
        self.pymunk_espace.add(obstacle.corps, obstacle.representation)

    def ajouterLieuFerme(self, lieu_ferme):
        self.lieu_ferme = lieu_ferme

        sommet_bas_gauche = lieu_ferme.position
        sommet_bas_droit = lieu_ferme.position + Vec2d(lieu_ferme.largeur, 0)
        sommet_haut_gauche = lieu_ferme.position + Vec2d(0, lieu_ferme.hauteur)
        sommet_haut_droit = lieu_ferme.position + Vec2d(lieu_ferme.largeur, lieu_ferme.hauteur)
        sommet_porte_gauche = lieu_ferme.position + Vec2d(lieu_ferme.largeur * lieu_ferme.position_porte - lieu_ferme.largeur_porte / 2, 0)
        sommet_porte_droit = lieu_ferme.position + Vec2d(lieu_ferme.largeur * lieu_ferme.position_porte + lieu_ferme.largeur_porte /2, 0)


        corps_mur_haut = pymunk.Body(body_type=pymunk.Body.STATIC)
        mur_haut = pymunk.Segment(corps_mur_haut, sommet_haut_gauche, sommet_haut_droit, 0.0)
        self.pymunk_espace.add(corps_mur_haut, mur_haut)

        corps_mur_gauche = pymunk.Body(body_type=pymunk.Body.STATIC)
        mur_gauche = pymunk.Segment(corps_mur_gauche, sommet_haut_gauche, sommet_bas_gauche, 0.0)
        self.pymunk_espace.add(corps_mur_gauche, mur_gauche)

        corps_mur_droit = pymunk.Body(body_type=pymunk.Body.STATIC)
        mur_droit = pymunk.Segment(corps_mur_droit, sommet_bas_droit, sommet_haut_droit, 0.0)
        self.pymunk_espace.add(corps_mur_droit, mur_droit)

        corps_mur_bas_droit = pymunk.Body(body_type=pymunk.Body.STATIC)
        mur_bas_droit = pymunk.Segment(corps_mur_bas_droit, sommet_bas_droit, sommet_porte_droit, 0.0)
        self.pymunk_espace.add(corps_mur_bas_droit, mur_bas_droit)

        corps_mur_bas_gauche = pymunk.Body(body_type=pymunk.Body.STATIC)
        mur_bas_gauche = pymunk.Segment(corps_mur_bas_gauche ,sommet_bas_gauche, sommet_porte_gauche, 0.0)
        self.pymunk_espace.add(corps_mur_bas_gauche, mur_bas_gauche)
