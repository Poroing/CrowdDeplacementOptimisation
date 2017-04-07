import sys
sys.path.append('..')
from convertir_json_python import convertirJsonPython
from traitement import RecuperationDeDonnees, TraitementDeDonnees
import matplotlib.pyplot as plt
from source_personne import Source
from affichage import Afficheur

afficheur = Afficheur()

configuration = convertirJsonPython('../FichiersConfiguration/configuration_MPSI2_obstacle_devant_porte.json')
recuperation = RecuperationDeDonnees(configuration, temps_maximal=20, action_mise_a_jour_secondaire=afficheur.dessinerEspaceEtAttendre)
#recuperation.simulation.sources.append(Source(recuperation.simulation.espace, Vec2d(500, 750), 0.5))

def optimiser_porte_debit(taille_min, taille_max, n ):
    
    debit, taille_porte = [], []
    
    for k in range (n):
        
        
        
        configuration['lieu_ferme']['porte_largeur'] = taille_min + k*(taille_max - taille_min)
        
        recuperation.lancer()
        
        traitement = TraitementDeDonnees(recuperation.temps_de_sortie)
        
        debit.append (traitement.avoirDebitMoyen())
        
        taille_porte.append(taille_min + k*(taille_max - taille_min))
        
            
        
    return taille_porte, debit

