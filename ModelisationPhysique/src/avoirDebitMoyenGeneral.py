Identifiant ????, taille(longxlarg), type de salle, nombre personnes de départ, (sorties,taille des sorties) , (générateurs de personnes, debit de personnes)
--> identifiant -> % -> debit


##

def creerConfiguration(taille, type_de_salle, nombre_de_personnes, infos_sorties, info_generateurs):
    configuration = {
        "type": "",
    
        "lieu_ferme": {
            "salle": {},
            "porte": [],
            "salle_couloir": {}
        },
        "obstacles": {
            "rangs" : {},
            "particulier" : {
                "rectangles": [],
                "cercles" : [],
                "polygones": []
            }
        },
        "personnes": {
            "zone_apparition" : {},
            "sources": [],
            "caracteristiques": {
                    "rayon_min" : 18,
                    "rayon_max" : 21,
                    "masse_surfacique" : 1.8
            },
        
        },
        "mise_a_jour_par_seconde": 60
    }
    
    configuration.update({'type' : type_de_salle})
    configuration['lieu_ferme']['salle'].update({'salle_hauteur' : taille[0], 'salle_largeur' : taille[1]})
    configuration['personne'].update({'nombre' : nombre_de_personnes})
    for sortie in info_sorties :
        configuration['lieu_ferme']['porte'].append({'position' : sortie[0] , 'largeur' : sortie[1] , 'mur' : sortie[2]})
        
    for source in info_generateurs : 
        configuration['personnes']['caracteristiques'] = pers
        configuration['personnes']['sources'].append({'position' : source[0],
                                                    'periode' : source[1],
                                                    'rayon_min' : pers['rayon_min'],
                                                    'rayon_max' : pers['rayon_max'],
                                                    'masse_surfacique' : pers['masse_surfacique']})
        
    return configuration

def recupererMoyenne(configuration) :
    recuperation = RecuperationDeDonnees(
        configuration,
        arreter_apres_temps=True,
        temps_maximal=15)
    recuperation.lancer()
    traitement = TraitementDeDonnees(recuperation.temps_de_sortie)
    return traitement.avoirDebitMoyen()
    
def fonction_de_transfert(infos,nb_simul):
    sortie = [[] for _ in range (len(infos))]
    for salle in info :
        
        ratio = 1
        while ratio != 0 :
            configuration = creerConfiguration(**salle)
            for _ in range(nb_simul):
                moy = 0
                moy += recupererMoyenne(configuration)
            moy /= nb_simul
            sortie[id].append(moy)
            ratio -= 0.2
        
            
