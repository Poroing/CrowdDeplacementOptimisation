import pymunk
from representation import Rectangle
from fonctions_annexes import convertirMetresPixels
import math
import functools
import geometrie
import collections
import space_hash
from pymunk import Vec2d
import base
import itertools


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

class TestGradient(TestBase):
    #Ce test n'utilise pas la position_voulue

    treillis_interet = dict()

    @property
    def treilli_interet(self):
        return TestGradient.treillis_interet[self.espace]

    def avoirDirectionASuivre(self):
        return TestGradient.treillis_interet[self.espace].avoirGradiantPosition(
            self.position)

    def update(self, position):
        super().update(position)

        direction = self.avoirDirectionASuivre()
        
        #Si la direction est nul la personne s'est retrouvé dans un obstacle
        #On lui donne une direction arbitraire pour le sortire
        if direction == Vec2d(0, 0):
            direction = Vec2d(0, 1)

        direction.length = 25

        self.point_a_suivre = direction + self.position

        self.fin_update()

class TestParcoursLargeur(TestBase):
    '''Keywords Arguments: precision, valeur_defaut, cls_tableau, rayon,
            position, position_voulue, espace

        Permet de faciliter l'utilisation d'un parcours en largeur sur des
        QuadrillageEspace

        toute sous classe doivent definire
            `genererCaseAdjacentes`
            `genererDebutsEtValeurs`
            `assignerValeurCase`
    '''

    def __init__(self, **kwargs):
        self.precision = kwargs['precision']
        del kwargs['precision']

        self.valeur_defaut = kwargs['valeur_defaut']
        del kwargs['valeur_defaut']

        self.cls_tableau = kwargs['cls_tableau']
        del kwargs['cls_tableau']

        super().__init__(**kwargs)

    def initialiserTableau(self):
        tableau = self.cls_tableau(
            position=self.espace.lieu_ferme.position
                - 2 * Vec2d(self.precision, self.precision),
            hauteur=self.espace.lieu_ferme.hauteur + 4 * self.precision,
            largeur=self.espace.lieu_ferme.largeur + 4 * self.precision,
            precision=self.precision,
            valeur_defaut=self.valeur_defaut)

        base.parcoursEnLargeur(
            self.genererDebutsEtValeurs(tableau),
            self.genererCaseAdjacentesParcoursLargeur,
            self.assignerValeurCase,
            tableau)

        return tableau

    def caseEstAccessible(self, case_depart, case, tableau):
        info_lancer_rayon = self.espace.avoirInfoSurLancerRayon(
            tableau.avoirCentreCase(case_depart),
            tableau.avoirCentreCase(case))

        return info_lancer_rayon is None

    def genererCaseAdjacentesParcoursLargeur(self, case, tableau):
        '''Generes les cases adjacentes en prenant en comptes des obstacles'''
        for case_adjacentes in self.genererCaseAdjacentes(case):
            if self.caseEstAccessible(case, case_adjacentes, tableau):
                yield case_adjacentes
        
    def genererCaseAdjacentes(self, case):
        '''Generes les cases adjacentes sans prendre en comptes des obstacles'''
        raise NotImplementedError()

    def assignerValeurCase(self, case_voisine, case_courante, tableau):
        raise NotImplementedError()

    def genererDebutsEtValeurs(self, tableau):
        raise NotImplementedError()

class TestGradientObstacle(TestGradient):

    DISTANCE_CHARACTERISITQUE = convertirMetresPixels(0.05)
    DISTANCE_MAX_INFLUENCE = 3 * DISTANCE_CHARACTERISITQUE
    
    def transformetChampParRapportObstacle(self, tableau):
        valeur_characteristique = min(tableau.genererValeurs())

        for case in tableau.genererCases():
            info_point = self.espace.avoirInfoPoint(
                tableau.avoirCentreCase(case),
                TestGradientObstacle.DISTANCE_MAX_INFLUENCE)
            if info_point is None:
                continue
            valeur = valeur_characteristique * math.exp(-info_point.distance
                / TestGradientObstacle.DISTANCE_CHARACTERISITQUE)

            tableau[case] += valeur

class TestGradientLargeur(TestGradient, TestParcoursLargeur):

    PRECISION_CHAMP = convertirMetresPixels(0.1)
    INACCESSIBLE_VALEUR = -5e2

    def __init__(self, **kwargs):
        kwargs['precision'] = TestGradientLargeur.PRECISION_CHAMP
        kwargs['valeur_defaut'] = TestGradientLargeur.INACCESSIBLE_VALEUR
        kwargs['cls_tableau'] = space_hash.InterpolationChampScalaire

        super().__init__(**kwargs)

        self.initialiserTreillisInteretSiNecessaire()

    def genererDebutsEtValeurs(self, tableau):
        return zip(
            map(
                tableau.avoirCasePlusProche,
                self.espace.lieu_ferme.avoirCentrePortes()),
            itertools.cycle([0]))

    def genererCaseAdjacentes(self, case):
        raise NotImplementedError()

    def assignerValeurCase(self, case_voisine, case_courante, tableau):
        tableau[case_voisine] = tableau[case_courante] - 1

    def initialiserTreillisInteretSiNecessaire(self):
        if self.espace not in TestGradientLargeur.treillis_interet:
            self.initialiserTreillisInteret()

    def initialiserTreillisInteret(self):
        TestGradientLargeur.treillis_interet[self.espace] = self.initialiserTableau()


class TestGradientLargeurObstacle(TestGradientLargeur, TestGradientObstacle):

    def initialiserTreillisInteret(self):
        super().initialiserTreillisInteret()
        self.transformetChampParRapportObstacle(self.treilli_interet)
    
class TestChampVecteur(TestParcoursLargeur):
    '''Choisit le mouvement des agents après avoir créer un champ
        de vecteur vers la position voulue

        Toute sous classe doivent redéfinir la fonction `avoirCaseAdjacentes`
    '''

    champs = dict()
    PRECISION_CHAMP = convertirMetresPixels(0.2)

    def __init__(self, **kwargs):
        kwargs['precision'] = TestChampVecteur.PRECISION_CHAMP
        kwargs['valeur_defaut'] = Vec2d(1, 0)
        kwargs['cls_tableau'] = Champ

        super().__init__(**kwargs)

        self.initialiserChampsSiNecessaire()

    def update(self, position):
        super().update(position)

        direction = self.champ.avoirValeurPlusProche(self.position)
        self.point_a_suivre = direction + self.position

        self.fin_update()

    @property
    def champ(self):
        return TestChampVecteur.champs[self.espace]

    def initialiserChampsSiNecessaire(self):
        if self.espace not in TestChampVecteur.champs:
            TestChampVecteur.champs[self.espace] = self.initialiserTableau()

    def genererCaseAdjacentes(self, case):
        raise NotImplementedError()

    def assignerValeurCase(self, case_voisine, case_courante, tableau):
        return tableau.dirigerVecteurVers(
            case_voisine,
            tableau.avoirCentreCase(case_courante))

    def genererDebutsEtValeurs(self, tableau):
        for centre_sortie in self.espace.lieu_ferme.avoirCentrePortes():
            case_sortie = tableau.avoirCaseAvecCentrePlusProche(centre_sortie)
            vecteur = centre_sortie - tableau.avoirCentreCase(case_sortie)
            yield case_sortie, vecteur


class TestLargeurQuatreDirections(TestParcoursLargeur):

    def genererCaseAdjacentes(self, case):
        return case.genererCaseAdjacentes(base.Case.genererQuatreDirections())


class TestLargeurHuitDirections(TestParcoursLargeur):

    def genererCaseAdjacentes(self, case):
        return case.genererCaseAdjacentes(base.Case.genererHuitDirections())

class TestChampVecteurQuatreDirections(
        TestLargeurQuatreDirections,
        TestChampVecteur):
    pass

class TestChampVecteurHuitDirections(
        TestLargeurHuitDirections,
        TestChampVecteur):
    pass

class TestGradientLargeurQuatreDirections(
        TestLargeurQuatreDirections,
        TestGradientLargeur):
    pass

class TestGradientLargeurHuitDirections(
        TestLargeurHuitDirections,
        TestGradientLargeur):
    pass

class TestGradientLargeurObstacleQuatreDirections(
        TestLargeurQuatreDirections,
        TestGradientLargeurObstacle):
    pass
        
class TestLanceRayon(TestBase):
    '''Keywords Arguments: position, rayon, position_voulue, obstacle

        Aide pour la contruction de test essayant d'éviter un obstacle
        bloquant l'accès à la sortie.

        Dans le code quelque chose est acceptable si aller dans sa direction
        permer d'éviter l'obstacle bloquant.

        Toute sous classe doit redéfinir les fonction `est<...>Acceptable` selon
        ses besoins.
    '''

    def update(self, position):
        super().update(position)
        self.longueur_rayon = self.espace.lieu_ferme.avoirLongueurDiagonale() / 2
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

    def avoirPointImpactRayon(self, info_lancer_rayon):
        if info_lancer_rayon is None:
            return None
        return info_lancer_rayon.point

    def avoirPointImpactVersAngle(self, angle):
        return self.avoirPointImpactRayon(self.avoirLancerAvecAngle(0))

    def avoirObjetVersAngle(self, angle):
        return self.avoirObjetToucheParRayon(self.avoirLancerAvecAngle(angle))

    def ininitialiserObstacleBloquant(self):
        self.obstacle_bloquant = self.avoirObjetVersAngle(0)

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


class Champ(space_hash.SpaceHash):
    '''Keywords argument: precision, position, hauteur, largeur'''

    def __init__(self, **kwargs):
        kwargs['valeur_defaut'] = Vec2d(1, 0)
        super().__init__(**kwargs)

    def dirigerVecteurVers(self, case, point):
        if self[case] == Vec2d(0, 0):
            return

        centre = self.avoirCentreCase(case)
        longueur_actuelle = self[case].length
        self[case] = point - centre
        if self[case] == Vec2d(0, 0):
            return 
        self[case].length = longueur_actuelle

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
        self.ininitialiserObjetVersAngle()
        super().update(position)

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


class TestBordsObstacle(TestLanceRayon):

    def sommetEstAccessible(self, sommet):
        return not self.espace.cercleEstEnDehorsDeLieuFerme(sommet, self.rayon * 2)

    def update(self, position):
        super().update(position)

        if self.obstacle_bloquant is None:
            self.point_a_suivre = self.position_voulue
        else:
            point_impact = self.avoirPointImpactVersAngle(0)
            avoirDistanceAPointImpact = lambda sommet: sommet.get_distance(point_impact)

            sommets_accessible = filter(self.sommetEstAccessible, self.obstacle_bloquant.sommets)
            self.point_a_suivre = min(
                sommets_accessible,
                key=avoirDistanceAPointImpact,
                default=self.obstacle_bloquant.sommets[0])

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
