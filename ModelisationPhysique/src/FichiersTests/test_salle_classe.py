import sys
sys.path.append('..')
from convertir_json_python import convertirJsonPython
from traitement import RecuperationDeDonnees, TraitementDeDonnees
import matplotlib.pyplot as plt
from source_personne import Source
from affichage import Afficheur

afficheur = Afficheur()

configuration = convertirJsonPython('../FichiersConfiguration/couloir.json')
recuperation = RecuperationDeDonnees(configuration, temps_maximal=20, action_mise_a_jour_secondaire=afficheur.dessinerEspaceEtAttendre)
#recuperation.simulation.sources.append(Source(recuperation.simulation.espace, Vec2d(500, 750), 0.5))
        
recuperation.lancer()
traitement = TraitementDeDonnees(recuperation.temps_de_sortie)
print(traitement.avoirDebitMoyen())
TraitementDeDonnees.personnes_en_fonction_du_temps()
