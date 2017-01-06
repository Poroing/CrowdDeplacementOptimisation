from pymunk.vec2d import Vec2d
import pygame
import pymunk.pygame_util
import pygame.locals
from simulation_propre import ConstructeurSimulation
from convertir_json_python import convertirJsonPython

def dessinerEspace(ecran, simulation, option_dessin, horloge):
    for event in pygame.event.get():
        if event.type == pygame.locals.QUIT:
            exit()
    ecran.fill(pygame.color.THECOLORS['black'])
    simulation.espace.pymunk_espace.debug_draw(option_dessin)
    pygame.display.flip()   
    horloge.tick(simulation.mise_a_jour_par_seconde)

def test():
    horloge = pygame.time.Clock()

    ecran = pygame.display.set_mode((1000, 1000))
    option_dessin = pymunk.pygame_util.DrawOptions(ecran)

    constructeur = ConstructeurSimulation(convertirJsonPython('configuration_MPE.json'), lambda temps: print(temps, 'Sortie'))
    simulation = constructeur.simulation
    simulation.action_mise_a_jour = lambda simulation: dessinerEspace(ecran, simulation, option_dessin, horloge)
    simulation.lancer()

test()
