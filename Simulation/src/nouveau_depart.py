import math

import pymunk
from pymunk import Vec2d

tailleSortie = 1.5 #mètres

ParoiHaute = 1
ParoiDroite = 2
ParoiBasse = 3
ParoiGauche = 4

#la sortie est en bas mdr

class LieuFerme(object):

    def __init__(self, largeur, hauteur):
    '''
        Aruments:
        ensembleSommets: ensemble des sommets consécutifs
    '''
        
        self.largeur = largeur
        self.hauteur = hauteur
        
        
        
def ajouterSalleDansEspace (lieuFerme):
    sommetHG = Vec2d(0, lieuFerme.hauteur)
    sommetHD = Vec2d (lieuFerme.largeur, lieuFerme.hauteur)
    sommetBD = Vec2d (lieuFerme.largeur, 0)
    sommetBG = Vec2d (0, 0)
    sortieGauche = Vec2d (0, (lieuFerme.largeur - tailleSortie) /2)
    sortieDroite = Vec2d (0, (lieuFerme.largeur + tailleSortie)/2)
    
    corps = pymunk.Body(body_type=pymunk.Body.STATIC)
    mur1= pymunk.Segment(body, sommetHG, sommetHD, 0.0)
    mur2= pymunk.Segment(body, sommetHD, sommetBD, 0.0)
    mur3Gauche= pymunk.Segment(body, sommetBD, sortierDroite, 0.0)
    mur3Droit= pymunk.Segment(body, sortieDroite, sommetBG, 0.0)
    mur4= pymunk.Segment(body, sommetBG, sommetHG, 0.0)
        
        
    
