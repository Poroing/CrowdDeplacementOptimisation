import pymunk
from obstacle import ObstacleRectangulaire
from representation_categories import RepresentationCategorie
from personne import Personne
from pymunk.vec2d import Vec2d
import time


class Espace(pymunk.Space):

    DIRECTIONS = [ Vec2d(0, -1), Vec2d(-1, 0), Vec2d(0, 1), Vec2d(1, 0) ]

    def __init__(self):
        super().__init__()

        self.lieu_ferme = None
        self.ensemble_obstacle = []
        self.ensemble_personnes = []
        
    def avancer(self, delta):
        self.step(delta)
        
        for personne in self.ensemble_personnes:
            personne.update()

    def cercleEstEnDehorsDeLieuFerme(self, position, rayon):
        return any(map(self.lieu_ferme.pointEstAExterieur,
            map(lambda direction: position + rayon * direction, Espace.DIRECTIONS)))

    def avoirInfoSurLancerRayon(self, debut, fin, ignorer_personne=True):
        if ignorer_personne:
            filtre = pymunk.ShapeFilter(mask=pymunk.ShapeFilter.ALL_MASKS ^ RepresentationCategorie.PERSONNE.value)
        else:
            filtre = pymunk.ShapeFilter()

        return self.segment_query_first(debut, fin, 1, filtre)

    def pointEstDansObstacle(self, point):
        return (self.lieu_ferme.pointEstAExterieur(point)
            or any(map(lambda obstacle: obstacle.pointEstAInterieur(point),
                self.ensemble_obstacle))
            or any(map(lambda obstacle: obstacle.pointEstAInterieur(point),
                self.ensemble_personnes)))
    
    def ajouterPersonne(self, personne):
        self.ensemble_personnes.append(personne)
        self.add(personne.corps, personne)
        
    
    def ajouterObstacle(self, obstacle):
        self.ensemble_obstacle.append(obstacle)
        self.add(obstacle.corps, obstacle)
    
    
    
    def recupererSommets(self, porte):
        sommet1, sommet2 = 0,0
        lieu_ferme = self.lieu_ferme
        
        if porte['mur'] == 'bas':
            sommet1 = lieu_ferme.position + Vec2d (porte['position'] * lieu_ferme.largeur - porte['largeur'] /2, 0 )
            sommet2 = lieu_ferme.position + Vec2d (porte['position'] * lieu_ferme.largeur + porte['largeur'] /2, 0 )
        
        if porte['mur'] == 'gauche' :
            sommet1 = lieu_ferme.position + Vec2d (0, porte['position'] * lieu_ferme.hauteur - porte['largeur'] /2 )
            sommet2 = lieu_ferme.position + Vec2d (0, porte['position'] * lieu_ferme.hauteur + porte['largeur'] /2)
            
        if porte['mur'] == 'haut' :
            sommet1 = lieu_ferme.position + Vec2d (porte['position'] * lieu_ferme.largeur - porte['largeur'] /2, lieu_ferme.hauteur )
            sommet2 = lieu_ferme.position + Vec2d (porte['position'] * lieu_ferme.largeur + porte['largeur'] /2, lieu_ferme.hauteur )
        
        if porte['mur'] == 'droite' :
            sommet1 = lieu_ferme.position + Vec2d (lieu_ferme.largeur, porte['position'] * lieu_ferme.hauteur - porte['largeur'] /2 )
            sommet2 = lieu_ferme.position + Vec2d (lieu_ferme.largeur, porte['position'] * lieu_ferme.hauteur + porte['largeur'] /2)
            
        return sommet1, sommet2
    
    def ajouterLieuFerme(self, lieu_ferme):
        
        self.lieu_ferme = lieu_ferme
        
        s_bg = lieu_ferme.position
        s_bd = lieu_ferme.position + Vec2d(lieu_ferme.largeur, 0)
        s_hg = lieu_ferme.position + Vec2d(0, lieu_ferme.hauteur)
        s_hd = lieu_ferme.position + Vec2d(lieu_ferme.largeur, lieu_ferme.hauteur)
        sommets = { "gauche" : [s_bg, s_hg] , "droite": [s_bd, s_hd] , "haut" : [s_hg, s_hd] , "bas" : [s_bg, s_bd]}
        
        
        for porte in lieu_ferme.liste_portes :
            
            sommet1, sommet2 = self.recupererSommets(porte)
            
            sommets[porte['mur']].append(sommet1)
            sommets[porte['mur']].append(sommet2)
        
        sommets['gauche'].sort()
        sommets['droite'].sort()
        sommets['bas'].sort()
        sommets['haut'].sort()
        
        for k in range (0,len(sommets['bas'])-1, 2):

            segment_bas = pymunk.Body(body_type=pymunk.Body.STATIC)
            mur_segment_bas = pymunk.Segment(segment_bas, sommets['bas'][k], sommets['bas'][k+1], 0.0)
            self.add(segment_bas, mur_segment_bas)

        for k in range (0, len(sommets['gauche'])-1, 2):
            
            segment_gauche = pymunk.Body(body_type=pymunk.Body.STATIC)
            mur_segment_gauche = pymunk.Segment(segment_gauche, sommets['gauche'][k], sommets['gauche'][k+1], 0.0)
            self.add(segment_gauche, mur_segment_gauche)
        
        for k in range (0, len(sommets['haut'])-1, 2):
            
            segment_haut = pymunk.Body(body_type=pymunk.Body.STATIC)
            mur_segment_haut = pymunk.Segment(segment_haut, sommets['haut'][k], sommets['haut'][k+1], 0.0)
            self.add(segment_haut, mur_segment_haut)
            
        for k in range (0, len(sommets['droite'])-1,2):
            
            segment_droite = pymunk.Body(body_type=pymunk.Body.STATIC)
            mur_segment_droite = pymunk.Segment(segment_droite, sommets['droite'][k], sommets['droite'][k+1], 0.0)
            self.add(segment_droite, mur_segment_droite)
            
  
    
    