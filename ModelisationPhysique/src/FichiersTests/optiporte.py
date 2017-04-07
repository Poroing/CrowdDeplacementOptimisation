import sys
sys.path.append('..')
from convertir_json_python import convertirJsonPython
from traitement import RecuperationDeDonnees, TraitementDeDonnees
from source_personne import Source
from affichage import Afficheur
import matplotlib.pyplot as plt


afficheur = Afficheur()

configuration = convertirJsonPython('../FichiersConfiguration/configuration_MPSI2_obstacle_devant_porte.json')
#recuperation.simulation.sources.append(Source(recuperation.simulation.espace, Vec2d(500, 750), 0.5))

taille_min, taille_max, n = 0 , 5 * configuration['personnes']['rayon_max'], 10
    
debit, taille_porte = [], []
    
for k in range (n):
        

    recuperation = RecuperationDeDonnees(configuration, temps_maximal=10, action_mise_a_jour_secondaire=afficheur.dessinerEspaceEtAttendre)
        
    configuration['lieu_ferme']['porte_largeur'] = taille_min + k*(taille_max - taille_min)
        
    recuperation.lancer()
        
    traitement = TraitementDeDonnees(recuperation.temps_de_sortie)
        
    debit.append (traitement.avoirDebitMoyen())
        
    taille_porte.append(taille_min + k*(taille_max - taille_min))
        
            
plt.plot(debit, taille_porte)

