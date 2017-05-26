from pymunk.vec2d import Vec2d

IDENTIDIANT_COTE = [ 'gauche', 'haut', 'droite', 'bas' ]

class SimpleSegment(object):

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

    def __init__(self, position, largeur, hauteur):
        self.largeur = largeur
        self.hauteur = hauteur
        self.position = Vec2d(position)

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
