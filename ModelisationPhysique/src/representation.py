import pymunk
from pymunk.vec2d import Vec2d
from math import pi
from functools import partial
import operator
import geometrie

class Representation(pymunk.Shape):
    '''Doit être instancié avec 

    Keyword Arguments: position, corps'''

    def __init__(self, **kwargs):
        position = kwargs['position']
        corps = kwargs['corps']
        del kwargs['position']
        del kwargs['corps']
        self.corps = corps
        self.corps.position = Vec2d(position)

    def avoirCoordoneeAbsolueDepuisRelative(self, point):
        return self.position + point

    @property
    def corps(self):
        return self.body

    @corps.setter
    def corps(self, value):
        self.body = value

    @property
    def position(self):
        return self.corps.position

class RepresentationDynamique(Representation):
    '''Keyword Arguments: position, masse, moment'''

    def __init__(self, **kwargs):
        masse = kwargs['masse']
        moment = kwargs['moment']
        del kwargs['masse']
        del kwargs['moment']
        kwargs['corps'] = pymunk.Body(masse, moment)
        super().__init__(**kwargs)


class Polygon(Representation, pymunk.Poly):
    '''Keywords Arguments: sommets, position, corps'''
    
    def __init__(self, **kwargs):
        #Forcer d'appeler de cette façon car la représentation doit être
        #créé après poly pour que le corps soit initialisé correctement
        pymunk.Poly.__init__(self, None, kwargs['sommets'])
        del kwargs['sommets']
        super().__init__(**kwargs)

    @property
    def sommets(self):
        return list(map(
            self.avoirCoordoneeAbsolueDepuisRelative,
            self.avoirSommetsRelatif()))

    def avoirSommetsRelatif(self):
        return self.get_vertices()

    def genererAretes(self):
        for i in range(len(self.sommets) - 1):
             yield geometrie.SimpleSegment(self.sommets[i], self.sommets[i + 1])
        yield geometrie.SimpleSegment(self.sommets[-1], self.sommets[0])

    def avoirBaryCentre(self):
        return (1 / len(self.sommets)) * sum(self.sommets)

class Segment(Representation, pymunk.Segment):
    '''Keywords Arguments: point1, point2, corps'''
    

    def __init__(self, **kwargs):
        pymunk.Segment.__init__(self, None, kwargs['point1'], kwargs['point2'], 0)
        del kwargs['point1']
        del kwargs['point2']
        #Le corps d'un segment ne prend apparement pas en compte la position
        #On la met donc à 0 par défault
        kwargs['position'] = Vec2d(0, 0)
        super().__init__(**kwargs)

    @property
    def sommets(self):
        return [self.point1, self.point2]

    def genererAretes(self):
        yield geometrie.SimpleSegment(*self.sommets)

    @property
    def point1(self):
        return self.a

    @property
    def point2(self):
        return self.b
    

class Rectangle(Polygon):
    '''Keyword Arguments: hauteur, largeur, position, corps'''

    def __init__(self, **kwargs):
        self.largeur = kwargs['largeur']
        self.hauteur = kwargs['hauteur']
        del kwargs['largeur']
        del kwargs['hauteur']
        kwargs['position'] = kwargs['position'] + self.avoirCentreRelatif()
        kwargs['sommets'] = list(self.genererSommetsRelatifsPymunk())
        super().__init__(**kwargs)

    def genererSommetsRelatifs(self):
        return map(partial(operator.add, self.avoirCentreRelatif()),
            self.genererSommetsRelatifsPymunk())

    def genererSommetsRelatifsPymunk(self):
        yield Vec2d(-self.largeur / 2, -self.hauteur / 2)
        yield Vec2d(+self.largeur / 2, -self.hauteur / 2)
        yield Vec2d(+self.largeur / 2, +self.hauteur / 2)
        yield Vec2d(-self.largeur / 2, +self.hauteur / 2)

    def avoirCentreRelatif(self):
        return Vec2d(self.largeur / 2, self.hauteur / 2)

class Cercle(Representation, pymunk.Circle):
    '''Keyword aruments: position, corps, rayon'''

    def __init__(self, **kwargs):
        rayon = kwargs['rayon']
        del kwargs['rayon']
        #Forcer d'appeler de cette façon car la représentation doit être
        #créé après circle pour que le corps soit initialisé correctement
        pymunk.Circle.__init__(self, None, rayon)
        super().__init__(**kwargs)

    @property
    def rayon(self):
        return self.radius


class CercleDynamique(RepresentationDynamique, Cercle):
    '''Keyword Arguments: position, masse, rayon'''
    
    def __init__(self, **kwargs):
        
       
        rayon = kwargs['rayon']
        masse = 2*pi* (kwargs['masse_surfacique'])**2
        
        del kwargs['masse_surfacique']
        
        kwargs['masse'] = masse
        kwargs['moment'] = pymunk.moment_for_circle(masse, 0, rayon)
        
        super().__init__(**kwargs)
