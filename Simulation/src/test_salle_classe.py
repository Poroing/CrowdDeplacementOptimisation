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
stop_apres_temp = False

resultat_debit = open("resultat.txt", "w")

def cv_liste_into_texte(liste):
    sortie = ""
    for k in range(len(liste)) :
        sortie += str(liste[k])
        if k !=len(liste) -1 :
            sortie += " "
    return sortie

def ajouterTables(lieu_ferme, hauteur_range_tables=50, largeur_range_tables=275):
    position_range = 150
    
    while position_range + hauteur_range_tables <= lieu_ferme.hauteur :
        lieu_ferme.ensemble_obstacle.append(ObstacleRectangulaire(hauteur_range_tables, largeur_range_tables, (125,position_range)))
        lieu_ferme.ensemble_obstacle.append(ObstacleRectangulaire(hauteur_range_tables, largeur_range_tables, (500,position_range)))
        position_range += 100

def ajouterPersonnesAleatoirementDansLieuFerme(lieu_ferme, nombre_personnes):
    for _ in range(nombre_personnes):
        lieu_ferme.ensemble_personnes.append(
            Personne(Vec2d(random.randint(60, 40 + lieu_ferme.largeur),
                random.randint(60, 40 + lieu_ferme.hauteur)), lieu_ferme))

def mettreAJourTempsPersonne(lieu_ferme, temps_evenement, temps_personne):
        for index_personne, personne in enumerate(lieu_ferme.ensemble_personnes):
            if not(personne.estSortie()):
                temps_personne[index_personne] = round(temps_evenement,3)
            
        resultat_debit.write(str(round(temps_evenement, 3)))
        resultat_debit.write(" ")
        resultat_debit.write(cv_liste_into_texte(temps_personne))
        resultat_debit.write('\n')

def test():
    IMAGE_PAR_SECONDE = 60
    NOMBRE_PERSONNE = 50
    horloge = pygame.time.Clock()

    ecran = pygame.display.set_mode((1000, 1000))
    option_dessin = pymunk.pygame_util.DrawOptions(ecran)

    espace = pymunk.Space()
    lieu_ferme = LieuFerme(largeur_classe, hauteur_classe, Vec2d(50, 50), position_porte)
    ajouterTables(lieu_ferme)
    ajouterPersonnesAleatoirementDansLieuFerme(lieu_ferme, NOMBRE_PERSONNE)
    lieu_ferme.ajouterDansEspace(espace)
    
    tempsPersonne = [0 for _ in range (NOMBRE_PERSONNE)]
       
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
        
        tempsEvenement = time.time() - depart
        
        for personne in lieu_ferme.ensemble_personnes:
            personne.update()

        mettreAJourTempsPersonne(lieu_ferme, tempsEvenement, tempsPersonne)
        
        horloge.tick(IMAGE_PAR_SECONDE)
        
        if stop_apres_temp and tempsEvenement > 10 :
            running = False

        
        
        
        
        

test()
resultat_debit.close()
