import convertir_json_python
from lieu_ferme import LieuFerme
from personne import Personne
from obstacle_rectangulaire import ObstacleRectangulaire
from espace import Espace
from pymunk.vec2d import Vec2d
import pygame
import pymunk.pygame_util
import random
import pygame.locals

##
class ConstructeurSalle(object):
       
    def __init__(self, donnees_simulation):
        
        
        self.donnees_simulation = donnees_simulation
        
        self.espace = Espace()
        self.ajouterLieuFerme(self.espace, **self.donnees_simulation['lieu_ferme'])
        self.ajouterObstacles(self.espace, **self.donnees_simulation['obstacles'])
        
    
    def ajouterLieuFerme(self, espace, salle_hauteur=None, salle_largeur=None, porte_largeur=None, porte_position=None):
        
        espace.ajouterLieuFerme(LieuFerme(salle_largeur, salle_hauteur, Vec2d(50, 50), porte_position, porte_largeur))
        
    
    def ajouterObstacles(self,espace, obstacle_hauteur=None,obstacle_largeur=None, obstacle_distance_intermediaire=None,mur_rang_distance=None, obstacle_gauche_position_premier=None, obstacle_droit_position_premier=None  ):
        
        position_gauche_y = obstacle_gauche_position_premier
        position_droit_y = obstacle_droit_position_premier
        
        
        
        while position_gauche_y + 50 <=self.espace.lieu_ferme.hauteur :
            
            position_gauche = 50 + mur_rang_distance, position_gauche_y
            
            espace.ajouterObstacle(ObstacleRectangulaire(obstacle_hauteur,obstacle_largeur,position_gauche))
            position_gauche_y += obstacle_distance_intermediaire
            
        
        while position_droit_y + 50 <= self.espace.lieu_ferme.hauteur :
            
            position_droit = 50 + self.espace.lieu_ferme.largeur + mur_rang_distance, position_droit_y
            
            espace.ajouterObstacle(ObstacleRectangulaire( obstacle_hauteur,obstacle_largeur,position_droit))
            position_droit_y += obstacle_distance_intermediaire
        

        

  