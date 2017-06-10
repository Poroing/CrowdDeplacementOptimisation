from simulation import Simulation
import pymunk
import pygame.locals
import pygame
import pygame.font
import copy
import math
import base
import trajectoires
import matplotlib.pyplot as plt
import numpy as np
import pymunk.pygame_util
from pymunk.vec2d import Vec2d

class DebugDrawOptions(pymunk.pygame_util.DrawOptions):
    
    def __init__(self, ecran, police='monospace', taille_police=15):
        super().__init__(ecran)
        self.couleur_texte = pygame.color.THECOLORS['white']
        self.couleur_champ = pygame.color.THECOLORS['green']
        self.police = pygame.font.SysFont(police, taille_police)
        self.antialias = False

    @property
    def ecran(self):
        return self.surface

    def drawText(self, texte, position):
        label = self.police.render(texte, self.antialias, self.couleur_texte)
        self.ecran.blit(label, pymunk.pygame_util.to_pygame(position, self.ecran))

class TraceurTrajectoire(trajectoires.Trajectoire):

    def tracerTrajectoires(self):
        for abscices, ordonees in self.genererXYArrays():
            plt.plot(abscices, ordonees)

def afficherChampVectorielle(champ):
    X = np.array(list(map(champ.avoirPositionColonne, range(champ.nombre_colonnes))))
    Y = np.array(list(map(champ.avoirPositionLigne, range(champ.nombre_lignes))))

    U = np.array(base.creerListeDoubleDimension(
            champ.nombre_lignes,
            champ.nombre_colonnes)).astype(np.float)
    V =  np.array(base.creerListeDoubleDimension(
            champ.nombre_lignes,
            champ.nombre_colonnes)).astype(np.float)

    for i in range(champ.nombre_lignes):
        for j in range(champ.nombre_colonnes):
            U[i, j], V[i, j] = champ[base.Case(i, j)]

    plt.streamplot(X, Y, U, V)
    plt.show()

def afficherChampGradient(champ):
    X = np.array(list(map(champ.avoirPositionColonne, range(2, champ.nombre_colonnes - 3))))
    Y = np.array(list(map(champ.avoirPositionLigne, range(2, champ.nombre_lignes - 3))))

    U = np.array(base.creerListeDoubleDimension(
            champ.nombre_lignes - 5,
            champ.nombre_colonnes - 5)).astype(np.float)
    V =  np.array(base.creerListeDoubleDimension(
            champ.nombre_lignes - 5,
            champ.nombre_colonnes - 5)).astype(np.float)

    for i in range(champ.nombre_lignes - 5):
        for j in range(champ.nombre_colonnes - 5):
            try:
                U[i, j], V[i, j] = champ.avoirGradiantPosition(Vec2d(Y[i], X[j]))
            except IndexError:
                pass
    print(champ.nombre_lignes, champ.nombre_colonnes)

    plt.streamplot(X, Y, U, V)
    plt.show()
    

class Afficheur(object):

    def __init__(self, debug=True):
        pygame.font.init()

        self.horloge = pygame.time.Clock()
        self.debug = debug

        self.ecran = pygame.display.set_mode((1000, 950))
        self.option_dessin = DebugDrawOptions(self.ecran)

    def dessinerAdresseObstacles(self, simulation):
        for obstacle in simulation.espace.ensemble_obstacle:
            self.option_dessin.drawText(
                hex(id(obstacle)),
                obstacle.position)

    def dessinerIdentifiantsEcouteurs(self, simulation):
        for ecouteur in simulation.ecouteurs:
            self.option_dessin.drawText(
                str(ecouteur.identifiant),
                ecouteur.personne.position)

    def dessinerPointSuiviePersonne(self, simulation):
        taille_point = 10
        couleur_point = pygame.color.THECOLORS['red']
        for ecouteur in simulation.ecouteurs:
            self.option_dessin.draw_dot(
                taille_point,
                ecouteur.point_suivie_personne,
                couleur_point)
            self.option_dessin.drawText(
                str(ecouteur.identifiant),
                ecouteur.point_suivie_personne)

    def dessinerEspaceEtAttendre(self, simulation):
        
        commande = Simulation.AUCUN
        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                return Simulation.ARRET
            if event.type == pygame.locals.KEYDOWN and event.key == pygame.locals.K_p:
                commande = commande | Simulation.TOGGLE_PAUSE

        self.ecran.fill(pygame.color.THECOLORS['black'])
        simulation.espace.debug_draw(self.option_dessin)

        if self.debug:
            self.dessinerIdentifiantsEcouteurs(simulation)
            self.dessinerPointSuiviePersonne(simulation)
            self.dessinerAdresseObstacles(simulation)
        
        pygame.display.flip()   
        self.horloge.tick(simulation.mise_a_jour_par_seconde)

        return commande
