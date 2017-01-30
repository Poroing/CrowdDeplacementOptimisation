from simulation_propre import Simulation
import pymunk
import pygame.locals
import pygame


class Afficheur(object):

    def __init__(self):

        self.horloge = pygame.time.Clock()

        self.ecran = pygame.display.set_mode((1000, 900))
        self.option_dessin = pymunk.pygame_util.DrawOptions(self.ecran)

    def dessinerEspaceEtAttendre(self, simulation):
        
        commande = Simulation.AUCUN
        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                return Simulation.ARRET
            if event.type == pygame.locals.KEYDOWN and event.key == pygame.locals.K_p:
                commande = commande | Simulation.TOGGLE_PAUSE

        self.ecran.fill(pygame.color.THECOLORS['black'])
        simulation.espace.pymunk_espace.debug_draw(self.option_dessin)
        
        pygame.display.flip()   
        self.horloge.tick(simulation.mise_a_jour_par_seconde)

        return commande
