import pymunk
from obstacle import ObstacleRectangulaire, OsbtacleSegment
from representation_categories import RepresentationCategorie, avoirMasqueSansValeur
from personne import Personne
from pymunk.vec2d import Vec2d
import time
import geometrie

class Espace(pymunk.Space):

    DIRECTIONS = [ Vec2d(0, -1), Vec2d(-1, 0), Vec2d(0, 1), Vec2d(1, 0) ]

    def __init__(self):
        super().__init__()

        self.lieu_ferme = None
        self.ensemble_obstacle = []
        self.ensemble_personnes = []
        self.ensemble_murs = []

        #Pour eviter les calculs répété de distances entre des obstacles
        self.calculateur_distance = geometrie.CalculateurDistanceAvecCache()

        self.rappelle_personne_ajoute = lambda personne: None
        
    def avancer(self, delta):
        self.step(delta)
        
        for personne in self.ensemble_personnes:
            personne.update()

    def avoirDistanceEntre(self, obstacle1, obstacle2):
        return self.calculateur_distance.avoirDistanceEntre(
            obstacle1,
            obstacle2)

    def peutPasserEntre(self, rayon, obstacle1, obstacle2):
        return (
            self.calculateur_distance.avoirDistanceEntre(
                obstacle1,
                obstacle2)
            > rayon)

    def cercleEstEnDehorsDeLieuFerme(self, position, rayon):
        return any(map(self.lieu_ferme.pointEstAExterieur,
            map(lambda direction: position + rayon * direction, Espace.DIRECTIONS)))

    def avoirInfoSurLancerRayon(self, debut, fin, ignorer_personne=True):
        if ignorer_personne:
            filtre = pymunk.ShapeFilter(mask=avoirMasqueSansValeur(
                pymunk.ShapeFilter.ALL_MASKS,
                RepresentationCategorie.PERSONNE.value))
        else:
            filtre = pymunk.ShapeFilter()
        epaisseur_rayon = 1

        return self.segment_query_first(debut, fin, epaisseur_rayon, filtre)

    def pointEstDansObstacle(self, point):
        return (self.lieu_ferme.pointEstAExterieur(point)
            or any(map(lambda obstacle: obstacle.pointEstAInterieur(point),
                self.ensemble_obstacle))
            or any(map(lambda obstacle: obstacle.pointEstAInterieur(point),
                self.ensemble_personnes)))
    
    def ajouterPersonne(self, personne):
        self.ensemble_personnes.append(personne)
        self.add(personne.corps, personne)
        self.rappelle_personne_ajoute(personne)
    
    def ajouterObstacle(self, obstacle):
        self.ensemble_obstacle.append(obstacle)
        self.add(obstacle.corps, obstacle)
            
    def recupererSommetsPorte(self, porte):
        mur = self.lieu_ferme.avoirCote(porte['mur'])
        largeur_porte_pourcentage = porte['largeur'] / mur.avoirLongueur()

        pourcentage_sommet1 = porte['position'] - largeur_porte_pourcentage / 2
        pourcentage_sommet2 = porte['position'] + largeur_porte_pourcentage / 2
        sommet1 = mur.avoirPositionPourcentage(pourcentage_sommet1)
        sommet2 = mur.avoirPositionPourcentage(pourcentage_sommet2)
        return sommet1, sommet2

    def ajouterMurEtPortes(self, sommets):
        #Le tri étant lexicographique selon (x, y) et les sommets étant
        #soit à x constant soit à y constant on fait un .sort() pour
        #avoir leurs position sur le mur
        sommets.sort()
        for k in range (0, len(sommets) - 1, 2):
            self.ajouterObstacle(OsbtacleSegment(
                point1=sommets[k],
                point2=sommets[k + 1]))
        

    def ajouterLieuFerme(self, lieu_ferme):
        self.lieu_ferme = lieu_ferme
    
        sommets = {
            'gauche' :list(self.lieu_ferme.genererSommetsCote('gauche')),
            'droite' :list(self.lieu_ferme.genererSommetsCote('droite')),
            'bas' :list(self.lieu_ferme.genererSommetsCote('bas')),
            'haut' :list(self.lieu_ferme.genererSommetsCote('haut')),
        }

        
        for porte in self.lieu_ferme.liste_portes :
            
            sommet1, sommet2 = self.recupererSommetsPorte(porte)
            
            sommets[porte['mur']].append(sommet1)
            sommets[porte['mur']].append(sommet2)
        
        self.ajouterMurEtPortes(sommets['bas'])
        self.ajouterMurEtPortes(sommets['haut'])
        self.ajouterMurEtPortes(sommets['gauche'])
        self.ajouterMurEtPortes(sommets['droite'])
