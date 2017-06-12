import sys
sys.path.append('..')
from convertir_json_python import convertirJsonPython
from traitement import RecuperationDeDonnees, TraitementDeDonnees
from affichage import Afficheur
from fonctions_annexes import convertirMetresPixels



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
    y,x=0,0
    
    if hauteur == 'haut':
        y = 50 + hauteur_salle - rayon_personne_max
        
    if hauteur == 'milieu' :
        y =50 + hauteur_salle/2
        
    if hauteur == 'bas' :
        y = 50 + 2*rayon_personne_max
        
    if largeur == 'gauche':
        x = 50 + 2*rayon_personne_max
        
    if largeur == 'milieu':
        x = 50 + largeur_salle/2
        
    if largeur == 'bas' :
        x = 50 + largeur_salle - rayon_personne_max

    return x,y
        
        


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
    
    
    type = parametre[1]
    nombre_de_personnes = parametre[2]
    sorties = parametre[3]
    sources = parametre[4]
    
    largeur_salle = convertirMetresPixels(parametre[0][0])
    
    
    if type == 'salle_en_Y':
        
        couloir_horizontal = convertirMetresPixels(parametre[5][0])
        couloir_vertical = convertirMetresPixels(parametre[5][1])
        
        hauteur_salle = couloir_vertical + (largeur_salle - couloir_horizontal)/2
        
        configuration['lieu_ferme']['salle_couloir'].update({'largeur_horizontale' : couloir_horizontal, 'largeur_verticale' : couloir_vertical})
        
    if type == 'salle_en_T':
        
        couloir_horizontal = convertirMetresPixels(parametre[5][0])
        couloir_vertical = convertirMetresPixels(parametre[5][1])
        
        hauteur_salle = couloir_vertical + couloir_horizontal
        
        configuration['lieu_ferme']['salle_couloir'].update({'largeur_horizontale' : couloir_horizontal, 'largeur_verticale' : couloir_vertical})
        
    
    else :
        hauteur_salle = convertirMetresPixels(parametre[0][1])
        
    

    
    configuration.update({'type' : type })
    
    if type == 'salle_de_classe':
        
        configuration['obstacles'].update({"rangs" : {
            "hauteur" : 45,
            "distance_intermediaire" : 2*configuration['personnes']['caracteristiques']['rayon_max'],
            "distance_au_mur" : 4*configuration['personnes']['caracteristiques']['rayon_max'],
            "largeur_gauche" : largeur_salle/3,
            "largeur_droit" : largeur_salle/3,
            "position_debut_gauche" : hauteur_salle/3,
            "position_debut_droit" : hauteur_salle/3 }})
            
    
        
    
    configuration['lieu_ferme']['salle'].update({'salle_hauteur' : hauteur_salle , 'salle_largeur' : largeur_salle})
    
    configuration['personnes'].update({'nombre' : (int(nombre_de_personnes * proportion_personnes/100))})
    
    for numero_sortie, info_sortie in sorties.items() :
        
        mur, position = obtenir_position_sortie(info_sortie[0])
        configuration['lieu_ferme']['porte'].append({'position' : position , 'largeur' : info_sortie[1]*convertirMetresPixels(0.75) , 'mur' : mur})
        
    for identifiant_source, info_sources in sources.items() :
        pers = configuration['personnes']['caracteristiques']
        
        position = obtenir_position_source(info_sources[0], pers['rayon_max'], hauteur_salle, largeur_salle)
        
        configuration['personnes']['sources'].append({'position' : position,
                                                    'periode' : info_sources[1],
                                                    'rayon_min' : pers['rayon_min'],
                                                    'rayon_max' : pers['rayon_max'],
                                                    'masse_surfacique' : pers['masse_surfacique']})
        
    return configuration

def recupererMoyenne(configuration) :
    afficheur = Afficheur()
    recuperation = RecuperationDeDonnees(
        configuration,
        arreter_apres_temps=True,
        temps_maximal=15,
        action_mise_a_jour_secondaire=afficheur.dessinerEspaceEtAttendre)
    recuperation.lancer()
    traitement = TraitementDeDonnees(recuperation.temps_de_sortie)
    return traitement.avoirDebitMoyen()
    
def pregeneration_debit(salles,nb_simul):
    
    sortie = {}
    
    for identifiants,parametres in salles.items() :
        sortie.update({identifiants : {}})
        ratio = 100
    
        while ratio != 0 :
            print(identifiants, ratio)
            configuration = creerConfiguration(parametres, ratio)
            for _ in range(nb_simul):
                
                debit = 0
                debit += recupererMoyenne(configuration)
                
            debit /= nb_simul
            sortie[identifiants].update({ratio : {0 : debit}})
            
            
            ratio -= 20
            
    return sortie
        
            
