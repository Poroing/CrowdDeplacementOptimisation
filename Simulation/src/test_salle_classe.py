from lieu_ferme import LieuFerme
from personne import Personne
from obstacle_rectangulaire import ObstacleRectangulaire
from pymunk.vec2d import Vec2d
import pygame
import pymunk.pygame_util
import random
import pygame.locals
import os
import time


largeur_classe, hauteur_classe = 800,800
position_porte = 0.8
largeur_porte = 85 
largeur_mur, hauteur_mur = 275, 50
stop_apres_temp = False
resultat_debit = open("resultat.txt", "w")
##
def cv_liste_into_texte(liste):
    sortie = ""
    for k in range(len(liste)) :
        sortie += str(liste[k])
        if k !=len(liste) -1 :
            sortie += " , "
    return sortie
##

def ajouterTables(lieu_ferme):
    pos = 150
    
    while pos + 50 <= hauteur_classe :
        lieu_ferme.ensemble_obstacle.append(ObstacleRectangulaire(hauteur_mur,largeur_mur,(125,pos)))
        lieu_ferme.ensemble_obstacle.append(ObstacleRectangulaire(hauteur_mur,largeur_mur,(500,pos)))
        pos += 100
    

def test():
    IMAGE_PAR_SECONDE = 60
    NOMBRE_PERSONNE = 50
    horloge = pygame.time.Clock()

    ecran = pygame.display.set_mode((1000, 1000))
    option_dessin = pymunk.pygame_util.DrawOptions(ecran)

    espace = pymunk.Space()
    lieu_ferme = LieuFerme(largeur_classe,hauteur_classe,Vec2d(50, 50), position_porte )
    ajouterTables(lieu_ferme)
    lieu_ferme.ajouterDansEspace(espace)

    personnes = [ Personne(Vec2d(random.randint(60, 40+ lieu_ferme.largeur), random.randint(60, 40 + lieu_ferme.hauteur)), lieu_ferme) for _ in range(NOMBRE_PERSONNE) ]
    for personne in personnes:
        personne.ajouterDansEspace(espace)
    
    tempsPersonne = [0 for _ in range (50)]
       
    
    
    
    running = True
    depart = time.time()
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                running = False
        ecran.fill(pygame.color.THECOLORS['black'])
        espace.debug_draw(option_dessin)
        pygame.display.flip()   

        espace.step(1 / IMAGE_PAR_SECONDE)
        
        numeroPersonne = 0
        
        for personne in personnes:
            
            personne.update()
            if not(personne.estSortie()):
                
                tempsPersonne[numeroPersonne] = round(time.time() - depart,3)
            
            numeroPersonne+= 1
        resultat_debit.write(str(round(time.time() - depart, 3)))
        resultat_debit.write(" , ")
        resultat_debit.write(cv_liste_into_texte(tempsPersonne))
        
        resultat_debit.write('\n')
        
        horloge.tick(IMAGE_PAR_SECONDE)
        
        if stop_apres_temp and time.time() - depart > 10 :
            running = False

        
        
        
        
        

test()
resultat_debit.close()
