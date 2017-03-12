from traitement import RecuperationDeDonnees
from convertir_json_python import convertirJsonPython
from Lagrange import avoirFonctionInterpolatriceParIntervalle, enleverValeursProches
import matplotlib.pyplot as plt
import numpy as np
from affichage import Afficheur

affichage = Afficheur()

recuperation = RecuperationDeDonnees(convertirJsonPython('./configuration_MPSI2.json'),
    temps_maximal=10, action_mise_a_jour_secondaire=affichage.dessinerEspaceEtAttendre)
recuperation.lancer()

intermediaire_X = list(np.linspace(-10, 0, num=100)) + recuperation.temps_de_sortie
intermediaire_Y = [0] * 100 + list(range(len(recuperation.temps_de_sortie) + 1))


nouveau_temps_sortie_X, nouveau_temps_sortie_Y = enleverValeursProches(intermediaire_X,
    intermediaire_Y, 0.05)

fonction_interpolatrice = avoirFonctionInterpolatriceParIntervalle(nouveau_temps_sortie_X,
    nouveau_temps_sortie_Y, 10)

print(fonction_interpolatrice(5))

X = np.linspace(0, recuperation.temps_de_sortie[-1], num=500)
Y = list(map(fonction_interpolatrice, X))

print(X, Y)

plt.plot(X, Y)
plt.plot([0] + recuperation.temps_de_sortie, list(range(len(recuperation.temps_de_sortie) + 1)))
plt.show()
