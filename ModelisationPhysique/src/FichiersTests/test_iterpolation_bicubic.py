import sys
sys.path.append('..')
from convertir_json_python import convertirJsonPython
from traitement import RecuperationDeDonnees, TraitementDeDonnees
from affichage import Afficheur
import test_point_suivre
from personne import Personne

from pymunk.vec2d import Vec2d

import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np

Personne.TEST_DIRECTION = test_point_suivre.TestGradientLargeurHuitDirections

afficheur = Afficheur()

configuration = convertirJsonPython(
    '../FichiersConfiguration/MPSTAR.json')
        
recuperation = RecuperationDeDonnees(
    configuration,
    arreter_apres_temps=True,
    temps_maximal=20,
    action_mise_a_jour_secondaire=afficheur.dessinerEspaceEtAttendre)


espace = recuperation.simulation.espace
treillis = test_point_suivre.TestGradientLargeurQuatreDirections.treillis_interet[espace]

#import space_hash
#import base
#import random
#
#treillis1 = space_hash.InterpolationChampScalaire(
#    position=Vec2d(0, 0),
#    largeur=2,
#    hauteur=2,
#    precision=0.1,
#    valeur_defaut=0)
#
#for i in range(treillis.nombre_lignes):
#    for j in range(treillis.nombre_colonnes):
#        treillis[base.Case(i, j)] = random.random()

SIZE = 5 * 10**2

x = np.linspace(
    treillis.position.x + 2 * treillis.precision,
    treillis.position.x + treillis.largeur - 2 * treillis.precision,
    num=SIZE)

y = np.linspace(
    treillis.position.y + 2 * treillis.precision,
    treillis.position.y + treillis.hauteur - 2 * treillis.precision,
    num=SIZE)

X, Y = np.meshgrid(x, y)
z_x = np.zeros((SIZE, SIZE))
z_y = np.zeros((SIZE, SIZE))

for i in range(SIZE):
    for j in range(SIZE):
        z_x[i, j], z_y[i, j] = treillis.avoirGradientParInterpolationBicubic(Vec2d(X[i, j], Y[i, j]))

plt.streamplot(x, y, z_x, z_y)
plt.show()
