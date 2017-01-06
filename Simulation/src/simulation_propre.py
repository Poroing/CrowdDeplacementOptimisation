import time
import random
from lieu_ferme import LieuFerme
from personne import Personne
from obstacle_rectangulaire import ObstacleRectangulaire
from espace import Espace
from pymunk.vec2d import Vec2d
import pygame
import pymunk.pygame_util

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

class EcouteurPersonne(self):

    def __init__(self, personne, action):
        self.personne = personne
        self.action = action
        self.personne_deja_sortie = False

    def ecouter(self, temps):
        if not self.personne_deja_sortie and personne.estSortie():
            self.action(temps)

class ConstructeurSimulation(object):

    def __init__(self, donnees_simulation, action_sortie):
        constructeur_salle = ConstructeurSalle(donnees_simulation)
        self.simulation = Simulation(constructeur_salle.espace, donnees_simulation['mise_a_jour_par_seconde'], action_sortie)

    def contruirePersonneEtEcouteur(self, nombre_personnes):
        #Pour le moment on met un ecouteur sur chaque personne
        for _ in range(nombre_personnes):
            personne = Personne(Vec2d(random.randint(60, 40 + self.espace.lieu_ferme.largeur),
                random.randint(60, 40 + self.espace.lieu_ferme.hauteur)), self.espace))
            self.simulation.ecouteurs.append(EcouteurPersonne(personne, mettreAJourPersonneSortie))
            self.simulation.espace.ajouterPersonne(personne)

class Simulation(object):
    
    def __init__(self, espace, mise_a_jour_par_seconde, action_mise_a_jour):
        self.espace = espace
        self.mise_a_jour_par_seconde = mise_a_jour_par_seconde
        self.ecouteurs = []
        self.mise_a_jour_par_seconde = action_mise_a_jour

    def mettreAJour(self):
        self.espace.avancer(1 / self.mise_a_jour_par_seconde)
        temp_mise_a_jour = time.time() - self.debut_lancement
        for ecouteur in self.ecouteurs:
            ecouteur.ecouter(temp_mise_a_jour)
        self.mise_a_jour_par_seconde(self)

    def lancer(self):
        self.debut_lancement = time.time()
        while True:
            self.mettreAJour()

