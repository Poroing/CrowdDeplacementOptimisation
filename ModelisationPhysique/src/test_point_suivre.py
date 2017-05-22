from pymunk.vec2d import Vec2d
import pymunk
from representation import Rectangle
import math
import functools
import math


class TestBase(object):
    '''Keyword arguments: espace, position, rayon, position_voulue'''

    def __init__(self, **kwargs):
        self.rappelle_update = lambda test: None

        self.espace = kwargs['espace']
        del kwargs['espace']

        self.rayon = kwargs['rayon']
        del kwargs['rayon']

        self.position_voulue = kwargs['position_voulue']
        del kwargs['position_voulue']

        self.update(kwargs['position'])
        del kwargs['position']

        self.point_a_suivre = self.position_voulue


        super().__init__(**kwargs)

    def update(self, position):
        self.position = position

    def fin_update(self):
        self.rappelle_update(self)

class TestDichotomieCompactageObstacle(TestBase):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def update(self, position):
        pass
        


#TODO: Peut être éviter les mise à jour lorsque l'obstacle est loing
class TestDichotomie(TestBase):

    GAUCHE = 0
    DROITE = 1

    PRECISION = math.pi / 100

    def update(self, position):
        super().update(position)

        info_lancer_rayon = self.espace.avoirInfoSurLancerRayon(position,
            self.position_voulue)

        if info_lancer_rayon is None:
            self.point_a_suivre = self.position_voulue
        else:
            representation_bloquante = info_lancer_rayon.shape
            print(f'Repr {representation_bloquante}')
            angle_inferieur, angle_superieur = self.avoirBornesDichotomie(info_lancer_rayon)

            while abs(angle_superieur - angle_inferieur) > TestDichotomie.PRECISION:
                millieu = (angle_inferieur + angle_superieur) / 2
                info_lancer_rayon = self.avoirLancerAvecAngle(millieu)

                print(f'angle: {angle_inferieur} {angle_superieur}')

                if info_lancer_rayon is not None:
                    print(f'Shape hit {info_lancer_rayon.shape}')
                    

                if info_lancer_rayon is None or (
                        info_lancer_rayon is not None
                        and info_lancer_rayon.shape is not representation_bloquante):

                    angle_superieur = millieu
                else:
                    angle_inferieur = millieu

            self.point_a_suivre = self.avoirPointVersLequelLancer(angle_superieur)

    def avoirPointVersLequelLancer(self, angle):
        direction_dans_laquel_lancer = self.position_voulue - self.position
        direction_dans_laquel_lancer.rotate(angle)
        return direction_dans_laquel_lancer + self.position

    def avoirBornesDichotomie(self, info_lancer_rayon):
        return (self.avoirPremiereBorneDichotomie(info_lancer_rayon),
             self.avoirSecondeBorneDichotomie(info_lancer_rayon))

    def avoirPremiereBorneDichotomie(self, info_lancer_rayon):
        return - math.pi / 2

    def avoirSecondeBorneDichotomie(self, info_lancer_rayon):
        return math.pi / 2

    def avoirSecondeBorneDichotomieParRapportAuBarycentre(self,
        info_lancer_rayon):

        bary_centre_obstacle = info_lancer_rayon.shape.avoirBaryCentre()
        cote_barycentre = self.avoirCotePointParRapportALigne(
            bary_centre_obstacle,
            self.position,
            self.position_voulue)

        if cote_barycentre == TestDichotomie.GAUCHE:
            return - math.pi / 2
        return math.pi / 2

    def avoirLancerAvecAngle(self, angle):
        point_vers_lequel_lancer = self.avoirPointVersLequelLancer(angle)
        return self.espace.avoirInfoSurLancerRayon(
            self.position,
            point_vers_lequel_lancer)

    def avoirCotePointParRapportALigne(self, point, point_1_ligne, point_2_ligne):
        if (point - point_1_ligne).cross(point_2_ligne - point) > 0:
            return TestDichotomie.GAUCHE
        return TestDichotomie.DROITE
        


class TestBordsObstacle(TestBase):

    def sommetEstAccessible(self, sommet):
        return not self.espace.cercleEstEnDehorsDeLieuFerme(sommet, self.rayon * 2)

    #def avoirSommets

    def update(self, position):
        super().update(position)

        info_lancer_rayon = self.espace.avoirInfoSurLancerRayon(position,
            self.position_voulue)

        if info_lancer_rayon is None:
            self.point_a_suivre = self.position_voulue
        else:
            avoirDistanceAPointRayon = lambda sommet: sommet.get_distance(info_lancer_rayon.point)
            transformerEnCoordoneeGlobal = lambda sommet: info_lancer_rayon.shape.body.local_to_world(sommet)

            #Les segments n'on pas de sommets dont il faut faire une disjonction de cas 
            if isinstance(info_lancer_rayon.shape, pymunk.Segment):
                self.point_a_suivre = self.position_voulue
            elif isinstance(info_lancer_rayon.shape, Rectangle):
                sommets = list(map(transformerEnCoordoneeGlobal, info_lancer_rayon.shape.get_vertices()))
                sommets_accessible = filter(self.sommetEstAccessible, sommets)
                self.point_a_suivre = min(sommets_accessible, key=avoirDistanceAPointRayon, default=sommets[0])

        self.fin_update()

class TestProximite(TestBase):
    '''Keyword arguments: espace, position, rayon, position_voulue, nombre_point (16)'''

    COEFFICIENT_TEST = 3

    def __init__(self, **kwargs):
        if 'nombre_point' not in kwargs:
            kwargs['nombre_point'] = 16
        self.nombre_point = kwargs['nombre_point']
        del kwargs['nombre_point']

        super().__init__(**kwargs)
        
        self.ensemble_point = list(
            self.genererEnsemblePoint(rayon * TestProximite.COEFFICIENT_TEST))
        self.point_a_suivre = self.ensemble_point[0]

    def genererEnsemblePoint(self, rayon):
        for i in range(self.nombre_point):
            point_local_x = math.cos(2 * math.pi * i / self.nombre_point)
            point_local_y = math.sin(2 * math.pi * i / self.nombre_point)
            point_local = rayon * Vec2d(point_local_x, point_local_y)
            yield self.position + point_local
            

    def update(self, position):
        self.updatePosition(position)
        if self.espace.pointEstDansObstacle(self.point_a_suivre):
            self.updatePointASuivre()

        self.fin_update()

    def forceUpdate(self, position):
        self.updatePosition(position)
        self.updatePointASuivre()
        
    def updatePosition(self, position):
        for point in self.ensemble_point:
            point += position - self.position
        self.position = position

    def updatePointASuivre(self):
        self.point_a_suivre = self.avoirPointLibrePlusProcheSortie()
            
    def genererPointsLibres(self):
        return filter(lambda point: not self.espace.pointEstDansObstacle(point), self.ensemble_point)

    def avoirPointLibrePlusProcheSortie(self):
        return min(self.genererPointsLibres(),
            key=lambda p: p.get_distance(self.position_voulue),
            default=self.ensemble_point[0])
