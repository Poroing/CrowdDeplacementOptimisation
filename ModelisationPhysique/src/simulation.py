import time
import random
from lieu_ferme import LieuFerme
from personne import Personne
from obstacle import ObstacleRectangulaire, ObstacleCirculaire
from espace import Espace
from pymunk.vec2d import Vec2d
from random import randint
import pygame
import pymunk.pygame_util



class ConstructeurSalle(object):
       
    def __init__(self, donnees_simulation):
        self.donnees_simulation = donnees_simulation
        
        self.espace = Espace()
        self.ajouterLieuFerme(self.espace, **self.donnees_simulation['lieu_ferme'])
        self.ajouterObstacles(self.espace, **self.donnees_simulation['obstacles'])
        
    
    def ajouterLieuFerme(self, espace, salle_hauteur=None, salle_largeur=None,
            porte_largeur=None, porte_position=None):
        espace.ajouterLieuFerme(LieuFerme(salle_largeur, salle_hauteur, Vec2d(50, 50), porte_position,
            porte_largeur))
    
    def ajouterObstacles(self, espace, rangs=None, particulier=None):
        self.ajouterRangs(espace, **rangs)
        self.ajouterObstaclesParticulier(espace, particulier)

    def ajouterObstaclesParticulier(self, espace, obstacles):
        for obstacle in obstacles['rectangles']:
            espace.ajouterObstacle(ObstacleRectangulaire(
                hauteur = obstacle['height'],
                largeur = obstacle['width'],
                position = obstacle['position']))
        for obstacle in obstacles['cercles']:
            espace.ajouterObstacle(ObstacleCirculaire(
                rayon = obstacle['rayon'],
                position = obstacle['position']))


    def ajouterRangs(self, espace, obstacle_gauche_largeur=None, obstacle_droit_largeur = None,
            obstacle_hauteur = None, obstacle_distance_intermediaire=None,
            mur_rang_distance=None, obstacle_gauche_position_premier=None,
            obstacle_droit_position_premier=None):

        position_gauche_y = obstacle_gauche_position_premier
        position_droit_y = obstacle_droit_position_premier
        
        
        #on ajoute les ranges de gauche
        while position_gauche_y + 50 <=self.espace.lieu_ferme.hauteur :
            position_gauche = 50 + mur_rang_distance, position_gauche_y
            
            obstacle_gauche = ObstacleRectangulaire(
                hauteur = obstacle_hauteur,
                largeur = obstacle_gauche_largeur,
                position = position_gauche)

            espace.ajouterObstacle(obstacle_gauche)

            position_gauche_y += obstacle_distance_intermediaire + obstacle_hauteur
            
            
        #on ajoute les rangs à droite
        while position_droit_y + 50 <= self.espace.lieu_ferme.hauteur :
            position_droit_x = 50 + self.espace.lieu_ferme.largeur - obstacle_droit_largeur - mur_rang_distance
            position_droit = position_droit_x, position_droit_y
            
            obstacle_droit = ObstacleRectangulaire(
                hauteur = obstacle_hauteur,
                largeur = obstacle_droit_largeur,
                position = position_droit)
            espace.ajouterObstacle(obstacle_droit)

            position_droit_y += obstacle_distance_intermediaire + obstacle_hauteur

class EcouteurPersonne(object):

    def __init__(self, personne, action):
        self.personne = personne
        self.action = action
        self.personne_deja_sortie = False

    def ecouter(self, temps):
        if not self.personne_deja_sortie and self.personne.estSortie():
            self.personne_deja_sortie = True
            self.executerAction(temps)

    def executerAction(self, temps):
        #Seul moyen d'appeler la fonction self.action sans passer self comme
        #premier argument
        _action = self.action
        _action(temps)

class ConstructeurSimulation(object):

    def __init__(self, donnees_simulation, action_sortie):
        constructeur_salle = ConstructeurSalle(donnees_simulation)

        creer_ecouteur = lambda personne: EcouteurPersonne(personne, action_sortie)

        self.simulation = Simulation(constructeur_salle.espace,
            donnees_simulation['mise_a_jour_par_seconde'], creer_ecouteur)

        minimum_y = max(donnees_simulation['obstacles']['rangs']['obstacle_gauche_position_premier'],
            donnees_simulation['obstacles']['rangs']['obstacle_droit_position_premier'])

        self.contruirePersonneEtEcouteur(action_sortie, minimum_y = minimum_y ,**donnees_simulation['personnes'] )

    def contruirePersonneEtEcouteur(self, action_sortie, nombre=0, sources=None, minimum_y=0, rayon_min = 30, rayon_max = 30,masse_surfacique = 1.8):
        #Pour le moment on met un ecouteur sur chaque personne
        for _ in range(nombre):
            personne = Personne(masse_surfacique, randint(rayon_min, rayon_max), Vec2d(random.randint(60, 40 + self.simulation.espace.lieu_ferme.largeur),
                random.randint(50 + minimum_y, 40 + self.simulation.espace.lieu_ferme.hauteur)), self.simulation.espace)
            self.simulation.ecouteurs.append(EcouteurPersonne(personne, action_sortie))
            self.simulation.espace.ajouterPersonne(personne)

class Simulation(object):

    AUCUN = 0x0
    ARRET = 0x1
    TOGGLE_PAUSE = 0x2
    
    def __init__(self, espace, mise_a_jour_par_seconde, creer_ecouteur):
        self.espace = espace
        self.mise_a_jour_par_seconde = mise_a_jour_par_seconde
        self.ecouteurs = []
        self.sources = []
        self.action_mise_a_jour = lambda simulation: None
        self.en_marche = False
        self.creer_ecouteur = creer_ecouteur

    def mettreAJour(self):
        self.espace.avancer(1 / self.mise_a_jour_par_seconde)
        for ecouteur in self.ecouteurs:
            ecouteur.ecouter(self.temps_depuis_lancement)
        self.mettreAJourSource()

    def gererActionExterieur(self):
        commande = self.action_mise_a_jour(self)
        self.executerCommande(commande)

    def gererTemps(self):
        if not self.en_pause:
            self.temps_depuis_lancement += time.time() - self.temps_derniere_boucle
        self.temps_derniere_boucle = time.time()
        

    def mettreAJourSource(self):
        for source in self.sources:
            personne_ajoute = source.mettreAJour(self.temps_depuis_lancement)
            if personne_ajoute is not None:
                self.ecouteurs.append(self.creer_ecouteur(personne_ajoute))

    def executerCommande(self, commande):
        if commande & Simulation.ARRET:
            self.en_marche = False
        if commande & Simulation.TOGGLE_PAUSE:
            self.en_pause = not self.en_pause

    def lancer(self):
        self.debut_lancement = time.time()
        self.temps_derniere_boucle = time.time()
        self.temps_depuis_lancement = 0
        self.en_marche = True
        self.en_pause = False
        while self.en_marche:
            self.gererTemps()
            self.gererActionExterieur()
            if self.en_pause:
                continue
            self.mettreAJour()

