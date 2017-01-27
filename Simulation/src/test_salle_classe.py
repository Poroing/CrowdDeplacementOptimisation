import pygame
import pymunk.pygame_util
import pygame.locals
from simulation_propre import ConstructeurSimulation, Simulation
from convertir_json_python import convertirJsonPython
from traitement_propre import RecuperationDeDonnees
import matplotlib.pyplot as plt


horloge = pygame.time.Clock()

ecran = pygame.display.set_mode((1100, 1100))
option_dessin = pymunk.pygame_util.DrawOptions(ecran)

def dessinerEspaceEtAttendre(simulation):
    for event in pygame.event.get():
        if event.type == pygame.locals.QUIT:
            return Simulation.ARRET

    ecran.fill(pygame.color.THECOLORS['black'])
    simulation.espace.pymunk_espace.debug_draw(option_dessin)
    
    pygame.display.flip()   
    horloge.tick(simulation.mise_a_jour_par_seconde)

    return Simulation.AUCUN

configuration = convertirJsonPython('configuration_MPSTAR.json')
recuperation = RecuperationDeDonnees(configuration, 10, dessinerEspaceEtAttendre)
recuperation.lancer()

plt.plot([0] + recuperation.temps_de_sortie, list(range(len(recuperation.temps_de_sortie)+1)))
plt.show()

