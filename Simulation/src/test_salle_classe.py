import pygame
import pymunk.pygame_util
import pygame.locals
import pygame.key
from simulation_propre import ConstructeurSimulation, Simulation
from convertir_json_python import convertirJsonPython
from traitement_propre import RecuperationDeDonnees
import matplotlib.pyplot as plt
from source_personne import Source
from pymunk.vec2d import Vec2d


horloge = pygame.time.Clock()

ecran = pygame.display.set_mode((1000, 1000))
option_dessin = pymunk.pygame_util.DrawOptions(ecran)

def dessinerEspaceEtAttendre(simulation):
    commande = Simulation.AUCUN
    for event in pygame.event.get():
        if event.type == pygame.locals.QUIT:
            return Simulation.ARRET
        if event.type == pygame.locals.KEYDOWN and event.key == pygame.locals.K_p:
            commande = commande | Simulation.TOGGLE_PAUSE

    ecran.fill(pygame.color.THECOLORS['black'])
    simulation.espace.pymunk_espace.debug_draw(option_dessin)
    pygame.display.flip()   
    horloge.tick(simulation.mise_a_jour_par_seconde)

    return commande

configuration = convertirJsonPython('couloir.json')
recuperation = RecuperationDeDonnees(configuration, temps_maximal=10, action_mise_a_jour_secondaire=dessinerEspaceEtAttendre)
#recuperation.simulation.sources.append(Source(recuperation.simulation.espace, Vec2d(500, 750), 0.5))
        
recuperation.lancer()
plt.plot([0] + recuperation.temps_de_sortie, list(range(len(recuperation.temps_de_sortie) + 1)))
plt.show()
