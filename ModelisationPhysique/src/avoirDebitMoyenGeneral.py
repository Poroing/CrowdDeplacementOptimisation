Identifiant ????, taille(longxlarg), type de salle, nombre personnes de départ , (sorties,taille des sorties) , (générateurs de personnes, debit de personnes)
--> identifiant -> % -> debit


##

def obtenir_position_sortie(position_sortie):
    
    [mur, position] = position_sortie.split('_')
    
    if position == 'gauche' :
        position = 0.2
    
    if position == 'milieu' :
        position = 0.5
        
    if position == 'droite' :
        position = 0.8
        
    return mur, position
    
    
def obtenir_position_source(position_source, rayon_personne_max, hauteur_salle, largeur_salle):
    hauteur, largeur = position_source.split('_')
    x,y=0,0
    if hauteur == 'haut':
        y = 50 + hauteur_salle - 2* rayon_personne_max
        
    if hauteur == 'milieu' :
        y =50 + hauteur_salle/2
        
    if hauteur == 'bas' :
        y = 50 + 2*rayon_personne_max
        
    if largeur == 'gauche':
        x = 50 + 2*rayon_personne_max
        
    if largeur == 'milieu':
        x = 50 + largeur_salle/2
        
    if largeur == 'bas' :
        x = 50 + largeur_salle - 2*rayon_personne_max
        
        
        
        


def creerConfiguration(parametre, proportion_personnes):
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
    
    configuration.update({'type' : parametre[1] })
    
    configuration['lieu_ferme']['salle'].update({'salle_hauteur' : convertirMetresPixels(parametre[0][0]) , 'salle_largeur' : convertirMetresPixels(parametre[0][1])})
    
    configuration['personnes'].update({'nombre' : (parametre[2] * proportion_personnes)})
    
    for numero_sortie, info_sortie in parametre[3].items() :
        
        mur, position = obtenir_position_sortie(info_sortie[0])
        configuration['lieu_ferme']['porte'].append({'position' : position , 'largeur' : info_sortie[1]*convertirMetresPixels(0.75) , 'mur' : mur})
        
    for identifiant_source, info_sources in parametre[4].items() : 
    
        pers = configuration['personnes']['caracteristiques']
        
        position = obtenir_position_source(info_sources[0], pers['rayon_max'], parametre[0][0], parametre[0][1])
        
        configuration['personnes']['sources'].append({'position' : position,
                                                    'periode' : info_sources[1],
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
    
def pregeneration_debit(salles,nb_simul):
    
    sortie = {}
    
    for identifiants,parametres in salles.items() :
        sortie.update({identifiants : {}})
        ratio = 1
        while ratio != 0 :
            configuration = creerConfiguration(parametres, ratio)
            for _ in range(nb_simul):
                
                debit = 0
                debit += recupererMoyenne(configuration)
                
            debit /= nb_simul
            
            sortie['identifiants'].update({ratio : {0 : debit}})
            
            ratio -= 0.2
    return sortie
        
            
