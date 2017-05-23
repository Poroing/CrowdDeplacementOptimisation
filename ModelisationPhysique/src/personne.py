from pymunk.vec2d import Vec2d
from representation_categories import RepresentationCategorie
from representation import CercleDynamique
from test_point_suivre import TestBordsObstacle, TestProximite
import fonctions_annexes
import math
import pymunk
import operator
import itertools
from random import randint
from math import pi

class Personne(CercleDynamique):

    VITESSE_MAXIMALE = fonctions_annexes.convertirMetresPixels(2)
    COEFFICIENT_EVITEMENT = 0.4
    RAYON_DE_PROXIMITE = fonctions_annexes.convertirMetresPixels(1.5)

    def __init__(self, masse_surfacique, rayon, position, espace, test_direction_cls=TestBordsObstacle):
        super().__init__(masse_surfacique = masse_surfacique, rayon=rayon, position=position)
        
        
        self.force_deplacement = self.rayon * 10**4
        self.filter = pymunk.ShapeFilter(categories=RepresentationCategorie.PERSONNE.value)
        self.espace = espace
        self.test_direction = test_direction_cls(position = position, espace = espace, rayon = self.rayon,
            position_voulue = self.sortieLaPlusProche())
        self.densite = self.nouvelleDensite()
        self.vitesse_maximale_propre = Personne.VITESSE_MAXIMALE
        
    
    def sortieLaPlusProche(self):
        position = self.position
        liste_centres = self.espace.lieu_ferme.avoirCentrePortes()
        distmin = position.get_distance(liste_centres[0])
        centre_min = liste_centres[0]
        
        for centre in (liste_centres):
            dist = position.get_distance(centre)
            if dist < distmin :
                distmin, centre_min = dist, centre
                
        return centre_min
    
    def pointEstAInterieur(self, point):
        return point.get_distance(self.body.position) < self.rayon

    def personneEstTropProche(self, personne):    
        return (personne.body.position.get_distance(self.body.position)
            < (2 + Personne.COEFFICIENT_EVITEMENT) * self.rayon)

    def estTropProcheDePersonne(self):
        return any(map(lambda personne: self.personneEstTropProche(personne),
            self.espace.ensemble_personnes))

    def estSortie(self):
        return self.espace.lieu_ferme.pointEstAExterieur(self.position)

    def nouvelleDensite(self):
        position = self.position
        
        centres_personnes = self.espace.ensemble_personnes
        
        nombre_de_personnes_a_proximite = 0
        
        for agent in self.espace.ensemble_personnes :
            
            if position.get_distance(agent.position) < Personne.RAYON_DE_PROXIMITE :
                
                nombre_de_personnes_a_proximite += 1
        
        return nombre_de_personnes_a_proximite /( pi* (Personne.RAYON_DE_PROXIMITE)**2)
            
    def miseAJourVitesseMax(self):
        densite = self.densite
        if densite == 0 :
            self.vitesse_maximale_propre =  Personne.VITESSE_MAXIMALE
        else :
            self.vitesse_maximale_propre = fonctions_annexes.convertirMetresPixels( 2 - min(1, densite**(-0.8)))
        
        
    def traiterVitesse(self):
        if self.corps.velocity.length > self.vitesse_maximale_propre :
            # On doit multiplier par un coefficient pour garder la direction du vecteur.
            self.corps.velocity *= self.vitesse_maximale_propre / self.body.velocity.length 

    def update(self):
        self.nouvelleDensite()
        self.miseAJourVitesseMax()
        self.traiterVitesse()
        if not self.estSortie():
            self.test_direction.update(self.body.position)
            force = (self.test_direction.point_a_suivre - self.body.position).normalized() * self.force_deplacement
            self.body.apply_force_at_local_point(force, Vec2d(0, 0))
