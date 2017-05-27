from pymunk.vec2d import Vec2d
import pymunk
from representation import Rectangle
import math
import functools
import geometrie


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

        Aide pour la contruction de test essayant d'éviter un obstacle
        bloquant l'accès à la sortie.

        Dans le code quelque chose est acceptable si aller dans sa direction
        permer d'éviter l'obstacle bloquant.

        Toute sous classe doit redéfinir les fonction `est<...>Acceptable` selon
        ses besoins.
    '''

    COEFFICIENT_LONGUEUR_INITIAL = 4

    def update(self, position):
        super().update(position)
        self.longueur_rayon = self.rayon * TestLanceRayon.COEFFICIENT_LONGUEUR_INITIAL
        self.ininitialiserObstacleBloquant()

    def avoirPositionVersAngle(self, angle):
        direction = (self.position_voulue - self.position)
        direction.length = self.longueur_rayon
        direction.rotate(angle)
        return direction + self.position

    def avoirLancerAvecAngle(self, angle):
        point_vers_lequel_lancer = self.avoirPositionVersAngle(angle)
        return self.espace.avoirInfoSurLancerRayon(
            self.position,
            point_vers_lequel_lancer)

    def avoirObjetToucheParRayon(self, info_lancer_rayon):
        if info_lancer_rayon is None:
            return None
        return info_lancer_rayon.shape

    def avoirObjetVersAngle(self, angle):
        return self.avoirObjetToucheParRayon(self.avoirLancerAvecAngle(angle))

    def ininitialiserObstacleBloquant(self):
        info_lancer_rayon = self.avoirLancerAvecAngle(0)
        if info_lancer_rayon is None:
            self.obstacle_bloquant = None
        else:
            self.obstacle_bloquant = info_lancer_rayon.shape

    def estAngleAcceptable(self, angle):
        objet_vers_angle = self.avoirObjetVersAngle(angle)
        return self.estObjetAcceptable(objet_vers_angle)

    def estObjetAcceptable(self, objet):
        return objet is None or objet is not self.obstacle_bloquant

    def estRayonAcceptable(self, info_lancer_rayon):
        return self.estObjetAcceptable(
            self.avoirObjetToucheParRayon(info_lancer_rayon))

    def angleEstPlusProcheDeSortie(self, angle, autre_angle):
        return (geometrie.avoirDistanceAngulaire(angle, 0)
            < geometrie.avoirDistanceAngulaire(autre_angle, 0))

    def avoirMeilleureAngleEntre(self, angle1, angle2):
        if self.angleEstPlusProcheDeSortie(angle1, angle2):
            return angle1
        return angle2


class TestLineaire(TestLanceRayon):
    '''Keyword Arguments: position, rayon, position_voulue, espace

        Les sous classes ne doivent pas redéfinir `update` sinon
        elles doivent appeler `TestLanceRayon.update(self, position)`
        au début de leur `update` au lieu de `super().update(position)`
    '''

    PRECISION = math.pi / 100

    def update(self, position):
        super().update(position)
        
        meilleur_angle = math.pi

        for i in range(0, self.avoirNombreRayon()):
            angle_courant = i * TestLineaire.PRECISION
            if self.angleEstPlusProcheDeSortie(meilleur_angle, angle_courant):
                continue
            if self.estAngleAcceptable(angle_courant):
                meilleur_angle = angle_courant

        if meileur_point_a_suivre is None:
            meileur_point_a_suivre = self.position_voulue

        self.point_a_suivre = self.avoirPositionVersAngle(meilleur_angle)

        self.fin_update()

    def avoirNombreRayon(self):
        return math.floor((2 * math.pi) / TestLineaire.PRECISION)

class TestRetiensObjet(TestLanceRayon):
    '''Permet le retient des objet présent dans la direction
        d'un angle pendant le temps d'une update,
        a utiliser pour les tests devant accéder plusieurs fois à cette
        information
    '''

    def update(self, position):
        super().update(position)
        self.ininitialiserObjetVersAngle()

    def ininitialiserObjetVersAngle(self):
        self.objet_vers_angle = dict()

    def avoirObjetVersAngle(self, angle):
        if angle not in self.objet_vers_angle:
            info_lancer_rayon = self.avoirLancerAvecAngle(angle)
            objet = self.avoirObjetToucheParRayon(info_lancer_rayon)
            self.objet_vers_angle[angle] = objet
        return self.objet_vers_angle[angle]


class TestDichotomie(TestRetiensObjet):

    PRECISION = math.pi / 100

    def update(self, position):
        super().update(position)

        if self.obstacle_bloquant is None:
            self.point_a_suivre = self.position_voulue
            self.fin_update()
            return

        #Il faut ajouter un décalage avec précision pour être sur que le
        #milieu se trouvera au bon endroit dans la dichotomie
        meilleur_angle = self.avoirMeilleureAngleEntre(
            self.avoirMeilleureAngleDansIntervalle(
                0, math.pi - TestDichotomie.PRECISION),
            self.avoirMeilleureAngleDansIntervalle(
                0, math.pi + TestDichotomie.PRECISION))

        self.point_a_suivre = self.avoirPositionVersAngle(meilleur_angle)

        self.fin_update()

    def avoirMeilleureAngleDansIntervalle(self, angle1, angle2):
        if (geometrie.avoirDistanceAngulaire(angle1, angle2) 
                < TestDichotomie.PRECISION):
            return angle1

        if geometrie.avoirDistanceAngulaire(angle1, angle2) > math.pi:
            raise ValueError('''Une dichotomie doit se faire sur des angles
                proche d'au moint pi''')

        if (self.estAngleAcceptable(angle1) 
                and self.estAngleAcceptable(angle2)):
            raise RuntimeError('Il n\'est pas possible d\'avoir des objet '
                + 'acceptable sur les deux borne de la dichotomie')

        milieu = geometrie.avoirMilieuProche(angle1, angle2)

        if (not self.estAngleAcceptable(angle1)
                and not self.estAngleAcceptable(angle2)):
            return self.avoirMeilleureAngleEntre(
                self.avoirMeilleureAngleDansIntervalle(angle1, milieu),
                self.avoirMeilleureAngleDansIntervalle(milieu, angle2))

        if self.estAngleAcceptable(angle1):
            if self.estAngleAcceptable(milieu):
                return self.avoirMeilleureAngleDansIntervalle(milieu, angle2)
            else:
                return self.avoirMeilleureAngleDansIntervalle(angle1, milieu)
        else:
            if self.estAngleAcceptable(milieu):
                return self.avoirMeilleureAngleDansIntervalle(milieu, angle1)
            else:
                return self.avoirMeilleureAngleDansIntervalle(angle2, milieu)


class TestCompactageObstacle(TestBase):
    '''Keyword Arguments: position, rayon, espace, position_voulue
        
        Associe à chaque obstacle les obstacles étant trop proche pour qu'un
        disque de rayon `self.rayon` puisse passer entre les deux obstacles
    '''

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.initialiserObstacleCompacte()

    def sontConsidererMemeObstacle(self, obstacle1, obstacle2):
        return not self.espace.peutPasserEntre(
            self.rayon,
            obstacle1,
            obstacle2)

    def initialiserObstacleCompacte(self):
        self.obstacle_compactes = dict()
        for obstacle in self.espace.ensemble_obstacle:
            ensemble_compacte = set()
            for autre_obstacle in self.espace.ensemble_obstacle:
                if (autre_obstacle is obstacle
                        or self.sontConsidererMemeObstacle(obstacle, autre_obstacle)):
                    ensemble_compacte.add(autre_obstacle)
            self.obstacle_compactes[obstacle] = frozenset(ensemble_compacte)


class TestLanceCompactageObstacle(TestLanceRayon, TestCompactageObstacle):

    def obstacleEstCompacteAvecObstacleBloquant(self, obstacle):
        return obstacle in self.obstacle_compactes[self.obstacle_bloquant]

    def estObjetAcceptable(self, objet):
        return (objet is None
            or not self.obstacleEstCompacteAvecObstacleBloquant(objet))

class TestLineaireCompactageObstacle(TestLanceCompactageObstacle, TestLineaire):
    pass
                
class TestDichotomieCompactageObstacle(TestLanceCompactageObstacle, TestDichotomie):
    pass


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
