from lieu_ferme import LieuFerme
from personne import Personne
from obstacle_rectangulaire import ObstacleRectangulaire
from espace import Espace
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

def ajouterTables(espace, hauteur_range_tables=50, largeur_range_tables=275):
    position_range = 150
    
    while position_range + hauteur_range_tables <= espace.lieu_ferme.hauteur :
        espace.ajouterObstacle(ObstacleRectangulaire(hauteur_range_tables, largeur_range_tables, (125,position_range)))
        espace.ajouterObstacle(ObstacleRectangulaire(hauteur_range_tables, largeur_range_tables, (500,position_range)))
        position_range += 100

def ajouterPersonnesAleatoirementDansEspace(espace, nombre_personnes):
    for _ in range(nombre_personnes):
        espace.ajouterPersonne(
            Personne(Vec2d(random.randint(60, 40 + espace.lieu_ferme.largeur),
                random.randint(60, 40 + espace.lieu_ferme.hauteur)), espace))

def mettreAJourTempsPersonne(espace, temps_evenement, temps_personne):
        for index_personne, personne in enumerate(espace.ensemble_personnes):
            if not(personne.estSortie()):
                temps_personne[index_personne] = round(temps_evenement,3)
            
        resultat_debit.write(str(round(temps_evenement, 3)))
        resultat_debit.write(" ")
        resultat_debit.write(cv_liste_into_texte(temps_personne))
        resultat_debit.write('\n')

def dessinerEspace(espace, option_dessin):
    espace.pymunk_espace.debug_draw(option_dessin)

def test():
    IMAGE_PAR_SECONDE = 60
    NOMBRE_PERSONNE = 50
    horloge = pygame.time.Clock()

    ecran = pygame.display.set_mode((1000, 1000))
    option_dessin = pymunk.pygame_util.DrawOptions(ecran)

    espace = Espace()
    espace.ajouterLieuFerme(LieuFerme(largeur_classe, hauteur_classe, Vec2d(50, 50), position_porte))
    ajouterTables(espace)
    ajouterPersonnesAleatoirementDansEspace(espace, NOMBRE_PERSONNE)
    
    tempsPersonne = [0 for _ in range (NOMBRE_PERSONNE)]
       
    running = True
    depart = time.time()
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                running = False

        ecran.fill(pygame.color.THECOLORS['black'])
        dessinerEspace(espace, option_dessin)
        pygame.display.flip()   

        espace.avancer(1 / IMAGE_PAR_SECONDE)
        
        tempsEvenement = time.time() - depart

        mettreAJourTempsPersonne(espace, tempsEvenement, tempsPersonne)
        
        horloge.tick(IMAGE_PAR_SECONDE)
        
        if stop_apres_temp and tempsEvenement > 10 :
            running = False

test()
resultat_debit.close()
