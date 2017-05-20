import sys
sys.path.append('..')
from simulation import ConstructeurSimulation, Simulation
from convertir_json_python import convertirJsonPython
from traitement import RecuperationDeDonnees
import matplotlib.pyplot as plt
from source_personne import Source
from affichage import Afficheur


def avoirTempsDeSortieMoyen(config, nombre):
    
    resultats = []
    
    for _ in range (nombre):


        afficheur = Afficheur()

        recuperation = RecuperationDeDonnees(config, temps_maximal=15, action_mise_a_jour_secondaire=afficheur.dessinerEspaceEtAttendre)
        recuperation.lancer()
    
        if resultats == [] :
            
            resultats = recuperation.temps_de_sortie
        
        else :
        
            for k in range (len(recuperation.temps_de_sortie)):
            
                resultats[k] += recuperation.temps_de_sortie[k]
            
    for k in range (len(resultats)):
            
        resultats[k] /= nombre
        
    return resultats
    
##


def avoirTempsSortieMoyenDeFichierConfiuration(chemin_acces_1, chemin_acces_2,n):
    config1 = convertirJsonPython(chemin_acces_1)
    config2 = convertirJsonPython(chemin_acces_2)
    
    return (resultats_moyens(config1,n),resultats_moyens(config2,n))
