from lieu_ferme import LieuFerme
from personne import Personne
from obstacle_rectangulaire import ObstacleRectangulaire
from pymunk.vec2d import Vec2d
import pygame
import pymunk.pygame_util
import random
import pygame.locals

largeur_classe, hauteur_classe = 800,800
largeur_porte = 85
largeur_mur, hauteur_mur = 275, 50


def test():
    IMAGE_PAR_SECONDE = 60
    NOMBRE_PERSONNE = 50
    horloge = pygame.time.Clock()

    ecran = pygame.display.set_mode((900, 900))
    option_dessin = pymunk.pygame_util.DrawOptions(ecran)

    espace = pymunk.Space()
    lieu_ferme = LieuFerme(largeur_classe,hauteur_classe,Vec2d(50, 50) )
    lieu_ferme.ajouterDansEspace(espace)

    personnes = [ Personne(Vec2d(random.randint(60, 40+ lieu_ferme.largeur), random.randint(60, 40 + lieu_ferme.hauteur)), lieu_ferme) for _ in range(NOMBRE_PERSONNE) ]
    for personne in personnes:
        personne.ajouterDansEspace(espace)
    
    pos = 125
    
    
    while pos + 50 <= hauteur_classe :
        murGauche = ObstacleRectangulaire(hauteur_mur,largeur_mur,(125,pos))
        murGauche.ajouterDansEspace(espace)
        murDroit = ObstacleRectangulaire(hauteur_mur,largeur_mur,(525,pos))
        murDroit.ajouterDansEspace(espace)
        pos += 110
        
    
    
    
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                running = False
        ecran.fill(pygame.color.THECOLORS['black'])
        espace.debug_draw(option_dessin)
        pygame.display.flip()

        espace.step(1 / IMAGE_PAR_SECONDE)
        for personne in personnes:
            personne.update()
        horloge.tick(IMAGE_PAR_SECONDE)

test()
