from pymunk.vec2d import Vec2d
import pymunk
from representation import Rectangle
import math
import functools
import math


class TestBase(object):
    '''Keyword arguments: espace, position, rayon, position_voulue

        Toute sous classe doit redéfinir la fonction `update` et
        appeler `fin_update` à la fin de la mise à jour
    '''

    def __init__(self, **kwargs):
        self.rappelle_update = lambda test: None

        self.espace = kwargs['espace']
        del kwargs['espace']

        self.rayon = kwargs['rayon']
        del kwargs['rayon']

        self.position_voulue = kwargs['position_voulue']
        del kwargs['position_voulue']

        self.position = kwargs['position']
        del kwargs['position']

        self.point_a_suivre = self.position_voulue

        super().__init__(**kwargs)


    def update(self, position):
        self.position = position

    def fin_update(self):
        self.rappelle_update(self)

class TestLanceRayon(TestBase):
    '''Keywords Arguments: position, rayon, position_voulue, obstacle

        Toute sous classe doit être redéfinir `rayonEstAcceptable` selon
        ses besoins
    '''

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def update(self, position):
        super().update(position)
        self.representation_bloquante = self.avoirRepresentationBloquante()

    def avoirPointVersLequelLancer(self, angle):
        direction_dans_laquel_lancer = self.position_voulue - self.position
        direction_dans_laquel_lancer.rotate(angle)
        return direction_dans_laquel_lancer + self.position

    def avoirLancerAvecAngle(self, angle):
        point_vers_lequel_lancer = self.avoirPointVersLequelLancer(angle)
        return self.espace.avoirInfoSurLancerRayon(
            self.position,
            point_vers_lequel_lancer)

    def avoirRepresentationBloquante(self):
        info_lancer_rayon = self.avoirLancerAvecAngle(0)
        if info_lancer_rayon is None:
            return None
        return info_lancer_rayon.shape

    def rayonEstAcceptable(self, info_lancer_rayon):
        return info_lancer_rayon is None

#TODO: Peut être éviter les mise à jour lorsque l'obstacle est loing
class TestDichotomie(TestLanceRayon):
    '''Keywords Arguments: position, position_voulue, rayon, espace

        Toute sous classe doit redéfinir `zoneSupe
    '''

    GAUCHE = 0
    DROITE = 1

    PRECISION = math.pi / 100

    def update(self, position):
        super().update(position)

        if self.representation_bloquante is None:
            self.point_a_suivre = self.position_voulue
        else:
            angle_inferieur, angle_superieur = self.avoirBornesDichotomie(info_lancer_rayon)

            while abs(angle_superieur - angle_inferieur) > TestDichotomie.PRECISION:
                millieu = (angle_inferieur + angle_superieur) / 2
                info_lancer_rayon = self.avoirLancerAvecAngle(millieu)

                if self.zoneSuperieurEstMeilleure(
                        info_lancer_rayon,
                        representation_bloquante):

                    angle_inferieur = millieu
                else:
                    angle_superieur = millieu

            self.point_a_suivre = self.avoirPointVersLequelLancer(angle_superieur)

    def zoneSuperieurEstMeilleure(self, info_lancer_rayon, representation_bloquante):
            return (info_lancer_rayon is not None
                and info_lancer_rayon.shape is representation_bloquante)

    def avoirBornesDichotomie(self, info_lancer_rayon):
        return (self.avoirPremiereBorneDichotomie(info_lancer_rayon),
             self.avoirSecondeBorneDichotomie(info_lancer_rayon))

    def avoirPremiereBorneDichotomie(self, info_lancer_rayon):
        return -math.pi / 2

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


    def avoirCotePointParRapportALigne(self, point, point_1_ligne, point_2_ligne):
        if (point - point_1_ligne).cross(point_2_ligne - point) > 0:
            return TestDichotomie.GAUCHE
        return TestDichotomie.DROITE


class TestLineaire(TestLanceRayon):
    '''Keyword Arguments: position, rayon, position_voulue, espace'''

    PRECISION = math.pi / 100

    def update(self, position):
        super().update(position)
        meileur_point_a_suivre = None
        meilleur_angle = math.pi

        for i in range(0, self.avoirNombreRayon()):
            angle_courant = i * TestLineaire.PRECISION
            if self.angleEstPlusProcheDeSortie(meilleur_angle, angle_courant):
                continue
            info_lancer_rayon = self.avoirLancerAvecAngle(angle_courant)
            if self.rayonEstAcceptable(info_lancer_rayon):
                meileur_point_a_suivre = self.avoirPointVersLequelLancer(angle_courant)
                meilleur_angle = angle_courant

        if meileur_point_a_suivre is None:
            meileur_point_a_suivre = self.position_voulue

        self.point_a_suivre = meileur_point_a_suivre
        self.fin_update()

    def avoirNombreRayon(self):
        return math.floor((2 * math.pi) / TestLineaire.PRECISION)

    def angleEstPlusProcheDeSortie(self, angle, autre_angle):
        return (self.avoirDistanceAngulaire(angle, 0)
            < self.avoirDistanceAngulaire(autre_angle, 0))

    def avoirDistanceAngulaire(self, angle, autre_angle):
        angle_centre = angle % (2 * math.pi)
        autre_angle_centre = autre_angle % (2 * math.pi)
        if angle_centre > autre_angle_centre:
            return self.avoirDistanceAngulaire(autre_angle, angle)
        distance = abs(angle_centre - autre_angle_centre)
        if distance > math.pi:
            autre_angle_centre -= 2 * math.pi
            distance = abs(autre_angle_centre - angle_centre)
        return distance               

class TestCompactageObstacle(TestBase):
    '''Keyword Arguments: position, rayon, espace, position_voulue
        
        Associe à chaque obstacle les obstacles étant trop proche pour qu'un
        disque de rayon `self.rayon` puisse passer entre les deux obstacles
    '''

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.initialiserObstacleCompacte()

    def initialiserObstacleCompacte(self):
        self.obstacle_compactes = dict()
        for obstacle in self.espace.ensemble_obstacle:
            ensemble_compacte = set()
            for autre_obstacle in self.espace.ensemble_obstacle:
                if not obstacle.peutEtrePasserEntre(self.rayon, autre_obstacle):
                    ensemble_compacte.add(autre_obstacle)
            self.obstacle_compactes[obstacle] = frozenset(ensemble_compacte)


class TestLanceCompactageObstacle(TestLanceRayon, TestCompactageObstacle):

    def obstacleEstCompacteAvecRepresentanteBloquante(self, obstacle):
        return obstacle in self.obstacle_compactes[self.representation_bloquante]

class TestLineaireCompactageObstacle(TestLanceCompactageObstacle, TestLineaire):

    def rayonEstAcceptable(self, info_lancer_rayon):
        return not (info_lancer_rayon is not None
            and self.obstacleEstCompacteAvecRepresentanteBloquante(
                info_lancer_rayon.shape))

                
class TestDichotomieCompactageObstacle(TestLanceCompactageObstacle, TestDichotomie):
            
    def zoneSuperieurEstMeilleure(self, info_lancer_rayon, representation_bloquante):
        return (info_lancer_rayon is not None
            and self.obstacleEstCompacteAvecRepresentanteBloquante(info_lancer_rayon.shape))


class TestBordsObstacle(TestBase):

    def sommetEstAccessible(self, sommet):
        return not self.espace.cercleEstEnDehorsDeLieuFerme(sommet, self.rayon * 2)

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
