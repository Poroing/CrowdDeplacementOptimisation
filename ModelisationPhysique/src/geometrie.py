from pymunk.vec2d import Vec2d
import base
import math

IDENTIDIANT_COTE = [ 'gauche', 'haut', 'droite', 'bas' ]

class SimpleSegment(object):
    #Permet de travailler avec aise sur les segments sans devoir instancier
    #une representation qui demande plus de place

    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2

    def avoirPositionPourcentage(self, pourcentage):
        return self.point1 + (self.point2 - self.point1) * pourcentage

    def avoirLongueur(self):
        return (self.point2 - self.point1).length

    def avoirPositionDistance(self, distance):
        return self.avoirPositionPourcentage(distance / self.avoirLongueur())

    def __repr__(self):
        return 'SimpleSegment({}, {})'.format(self.point1, self.point2)


class SimpleRectangle(object):
    #Permet de travailler avec aise sur les rectangles sans devoir instancier
    #une representation qui demande plus de place

    def __init__(self, position, largeur, hauteur):
        self.largeur = largeur
        self.hauteur = hauteur
        self.position = Vec2d(position)

    @property
    def sommets(self):
        ajouterPosition = lambda sommet: sommet + self.position
        return list(map(
            ajouterPosition,
            self.genererSommetsRelatifSensHoraireDepuisPosition()))

    def genererSommetsCote(self, identifiant_cote):
        ajouterPosition = lambda sommet: sommet + self.position
        return map(
            ajouterPosition,
            self.genererSommetsCoteRelatif(identifiant_cote))

    def genererSommetsCoteRelatif(self, identifiant_cote):
        GAUCHE = 0
        HAUT = 1
        DROITE = 2
        BAS = 3
        if identifiant_cote == 'bas':
            arrete = BAS
        elif identifiant_cote == 'gauche':
            arrete = GAUCHE
        elif identifiant_cote == 'droite':
            arrete = DROITE
        elif identifiant_cote == 'haut':
            arrete = HAUT

        sommets = list(self.genererSommetsRelatifSensHoraireDepuisPosition())
        return sommets[arrete], sommets[(arrete + 1) % 4]

    def avoirCote(self, identifiant_cote):
        return SimpleSegment(*self.genererSommetsCote(identifiant_cote))

    def genererSommetsRelatifSensHoraireDepuisPosition(self):
        yield Vec2d(0, 0)
        yield Vec2d(0, self.hauteur)
        yield Vec2d(self.largeur, self.hauteur)
        yield Vec2d(self.largeur, 0)

    def pointEstAExterieur(self, point):
        return ( point.x > self.position.x + self.largeur or point.x < self.position.x
            or point.y > self.position.y + self.hauteur or point.y < self.position.y)


class CalculateurDistanceAvecCache(object):
    '''Sers a mettre en cache les valeurs calculées pour éviter
        de calculer plusieurs fois la même distance
    ''' 

    def __init__(self):
        self.distances = base.KeyPairDict()

    def avoirDistanceEntre(self, polygon1, polygon2):
        if (polygon1, polygon2) in self.distances:
            return self.distances[(polygon1, polygon2)]
        distance = self.calculerDistanceEntre(polygon1, polygon2)
        self.distances[(polygon1, polygon2)] = distance
        return distance

    def calculerDistanceEntre(self, polygon1, polygon2):
        distance_min = polygon1.sommets[0].get_distance(polygon2.sommets[0])
        
        for sommet1 in polygon1.sommets:
            for sommet2 in polygon2.sommets:
                distance_min = min(distance_min, sommet1.get_distance(sommet2))
                

        for sommet in polygon1.sommets:
            for arete in polygon2.genererAretes():
                projection = avoirProjectionSurSegment(sommet, arete)
                if projection is None:
                    continue
                distance_min = min(distance_min, sommet.get_distance(projection))

        for sommet in polygon2.sommets:
            for arete in polygon1.genererAretes():
                projection = avoirProjectionSurSegment(sommet, arete)
                if projection is None:
                    continue
                distance_min = min(distance_min, sommet.get_distance(projection))

        return distance_min

def avoirDistanceAngulaire(angle, autre_angle):
    angle_centre = angle % (2 * math.pi)
    autre_angle_centre = autre_angle % (2 * math.pi)
    if angle_centre > autre_angle_centre:
        return avoirDistanceAngulaire(autre_angle, angle)
    distance = abs(angle_centre - autre_angle_centre)
    if distance > math.pi:
        autre_angle_centre -= 2 * math.pi
        distance = abs(autre_angle_centre - angle_centre)
    return distance               

def avoirMilieusAngulaire(angle1, angle2):
    '''Renvoie le milieu proche suivie du milieu eloigne'''
    angle1_centre = angle1 % (2 * math.pi)
    angle2_centre = angle2 % (2 * math.pi)

    milieu1 = (angle1_centre + angle2_centre) / 2
    milieu2 = milieu1 + math.pi
    if avoirDistanceAngulaire(milieu1, angle1) < math.pi / 2:
        milieu_proche = milieu1
        milieu_eloigne = milieu2
    else:
        milieu_proche = milieu2
        milieu_eloigne = milieu1
    return (milieu_proche, milieu_eloigne)

def avoirMilieuEloigne(angle1, angle2):
    return avoirMilieusAngulaire(angle1, angle2)[1]

def avoirMilieuProche(angle1, angle2):
    return avoirMilieusAngulaire(angle1, angle2)[0]

def centrerPoint(point, centre):
    return point - centre

def avoirPositionProjection(vecteur1, vecteur2):
    return vecteur1.dot(vecteur2) / vecteur2.get_length_sqrd()

def avoirProjectionSurSegment(point, segment):
    point_centre = centrerPoint(point, segment.point2)
    direction_segment_centre = centrerPoint(segment.point1, segment.point2)
    t = avoirPositionProjection(point_centre, direction_segment_centre)
    if t < 0 or t > 1:
        return None
    return direction_segment_centre * t + segment.point2
