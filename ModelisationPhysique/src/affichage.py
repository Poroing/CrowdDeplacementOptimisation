from simulation import Simulation
import pymunk
import pygame.locals
import pygame
import pygame.font
import copy
import math
import base

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

    def drawChamp(self, longueur_vecteur, champ, profondeur=None):
        if profondeur is None:
            profondeur = base.TableauDeuxDimension(
                nombre_lignes=champ.nombre_lignes,
                nombre_colonnes=champ.nombre_colonnes,
                valeur_defaut=0)

        for case in champ.genererCases():
            debut = champ.avoirCentreCase(case)
            direction = copy.copy(champ[case])
            direction.length = longueur_vecteur
            fin = debut + direction

            debut = pymunk.pygame_util.to_pygame(debut, self.ecran)
            fin = pymunk.pygame_util.to_pygame(fin, self.ecran)

            self.drawText(str(profondeur[case]), debut)

            pygame.draw.line(self.ecran, self.couleur_texte, debut, fin)
            pygame.draw.circle(
                self.ecran,
                self.couleur_champ,
                list(map(math.floor, fin)),
                longueur_vecteur // 2)

class Afficheur(object):

    def __init__(self):
        pygame.font.init()

        self.horloge = pygame.time.Clock()

        self.ecran = pygame.display.set_mode((1000, 900))
        self.option_dessin = DebugDrawOptions(self.ecran)

    def dessinerPremierChamp(self, simulation):
        #TODO: rendre cela moin dégueulasse
        from test_point_suivre import TestChampVecteur
        longueur_vecteur = 5
        self.option_dessin.drawChamp(
            longueur_vecteur,
            next(iter(TestChampVecteur.champs.values())))

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

        self.dessinerIdentifiantsEcouteurs(simulation)
        self.dessinerPointSuiviePersonne(simulation)
        self.dessinerAdresseObstacles(simulation)
        #self.dessinerPremierChamp(simulation)
        
        pygame.display.flip()   
        self.horloge.tick(simulation.mise_a_jour_par_seconde)

        return commande
