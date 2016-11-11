from salle_simplifie import Personne, LieuFermre
from pymunk.vec2d import Vec2d
import pygame
import pymunk.pygame_util
import random


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
        print('Running')
        ecran.fill(pygame.color.THECOLORS['black'])
        espace.debug_draw(option_dessin)
        pygame.display.flip()

        espace.step(1 / IMAGE_PAR_SECONDE)
        for personne in personnes:
            personne.update()
        horloge.tick(IMAGE_PAR_SECONDE)

test()
