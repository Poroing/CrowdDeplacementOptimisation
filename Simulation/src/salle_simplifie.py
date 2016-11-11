from pymunk.vec2d import Vec2d
import pymunk
import pygame
import pymunk.pygame_util
import random

class LieuFermre(object):

    def __init__(self, largeur, hauteur, position=(0, 0), largeur_porte=30):
        self.largeur = largeur
        self.hauteur = hauteur
        self.position = Vec2d(position)
        self.largeur_porte = largeur_porte

    def avoirCentrePorte(self):
        return self.position + Vec2d(self.largeur / 2, 0)

    def ajouterDansEspace(self, espace):
        sommet_bas_gauche = self.position
        sommet_bas_droit = self.position + Vec2d(self.largeur, 0)
        sommet_haut_gauche = self.position + Vec2d(0, self.hauteur)
        sommet_haut_droit = self.position + Vec2d(self.largeur, self.hauteur)
        sommet_porte_gauche = self.position + Vec2d((self.largeur - self.largeur_porte) / 2, 0)
        sommet_porte_droit = self.position + Vec2d((self.largeur + self.largeur_porte) / 2, 0)


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


class Personne(object):

    RAYON = 5
    MASSE = 70
    MOMENT = pymunk.moment_for_circle(MASSE, 0, RAYON)
    FORCE_DEPLACEMENT = 5 * 10**4
    VITESSE_MAXIMALE = 50

    def __init__(self, position, lieu_ferme):
        self.body = pymunk.Body(Personne.MASSE, Personne.MOMENT)
        self.shape = pymunk.Circle(self.body, Personne.RAYON)
        self.body.position = position
        
        self.lieu_ferme = lieu_ferme

    def ajouterDansEspace(self, espace):
        espace.add(self.body, self.shape)

    def traiterVitesse(self):
        if self.body.velocity.length > Personne.VITESSE_MAXIMALE:
            self.body.velocity *= Personne.VITESSE_MAXIMALE / self.body.velocity.length

    def update(self):
        self.traiterVitesse()
        force = (self.lieu_ferme.avoirCentrePorte() - self.body.position).normalized() * Personne.FORCE_DEPLACEMENT
        self.body.apply_force_at_local_point(force, Vec2d(0, 0))
            

def test():
    IMAGE_PAR_SECONDE = 60
    NOMBRE_PERSONNE = 60
    horloge = pygame.time.Clock()

    ecran = pygame.display.set_mode((200, 200))
    option_dessin = pymunk.pygame_util.DrawOptions(ecran)

    espace = pymunk.Space()
    lieu_ferme = LieuFermre(100, 100, Vec2d(50, 50))
    lieu_ferme.ajouterDansEspace(espace)

    personnes = [ Personne(Vec2d(random.randint(60, 140), random.randint(60, 140)), lieu_ferme) for _ in range(NOMBRE_PERSONNE) ]
    for personne in personnes:
        personne.ajouterDansEspace(espace)
    
    while True:
        ecran.fill(pygame.color.THECOLORS['black'])
        espace.debug_draw(option_dessin)
        pygame.display.flip()

        espace.step(1 / IMAGE_PAR_SECONDE)
        for personne in personnes:
            personne.update()
        horloge.tick(IMAGE_PAR_SECONDE)

test()
