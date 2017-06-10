import math
import itertools
import base
from pymunk.vec2d import Vec2d
import numpy as np

class QuadrillageEspace(base.TableauDeuxDimension):
    '''Keyword Arguments: precision, hauteur, largeur, position,
            valeur_defaut (None)

        Toute sous classe doit définir `avoirCentreCase`
    '''

    def __init__(self, **kwargs):
        self.precision = kwargs['precision']
        del kwargs['precision']

        self.position = kwargs['position']
        del kwargs['position']

        self.hauteur = kwargs['hauteur']
        del kwargs['hauteur']

        self.largeur = kwargs['largeur']
        del kwargs['largeur']

        kwargs['nombre_lignes'] = math.ceil(self.hauteur / self.precision)
        kwargs['nombre_colonnes'] = math.ceil(self.largeur / self.precision)

        super().__init__(**kwargs)

    def avoirCentreCase(self, case):
        return Vec2d(
            self.avoirPositionColonne(case.colonne),
            self.avoirPositionLigne(case.ligne))

    def avoirPositionLigne(self, ligne):
        raise NotImplementedError()

    def avoirPositionColonne(self, colonne):
        raise NotImplementedError()


class Treillis(QuadrillageEspace):

    def avoirCasePlusProche(self, point):
        return min(
            self.genererCasesEncadrante(point),
            key=lambda case: point.get_distance(self.avoirPositionCase(case)))

    def avoirPositionCase(self, case):
        position_relative = Vec2d(
            case.colonne * self.precision,
            case.ligne * self.precision)
        return self.position + position_relative

    def avoirPositionLigne(self, ligne):
        return self.position.y + ligne * self.precision

    def avoirPositionColonne(self, colonne):
        return self.position.x + colonne * self.precision

    def avoirLigneBasse(self, point):
        return math.floor((point.y - self.position.y) / self.precision)

    def avoirLigneHaute(self, point):
        return math.ceil((point.y - self.position.y) / self.precision)

    #De même
    def avoirColonneGauche(self, point):
        return math.floor((point.x - self.position.x) / self.precision)

    def avoirColonneDroite(self, point):
        return math.ceil((point.x - self.position.x) / self.precision)

    def genererCasesEncadrante(self, point):
        ligne_haute = self.avoirLigneHaute(point)
        ligne_basse = self.avoirLigneBasse(point)
        colonne_gauche = self.avoirColonneGauche(point)
        colonne_droite = self.avoirColonneDroite(point)

        yield base.Case(ligne_basse, colonne_gauche)
        yield base.Case(ligne_basse, colonne_droite)
        yield base.Case(ligne_haute, colonne_droite)
        yield base.Case(ligne_haute, colonne_gauche)

    def reglerConflitColonnes(self, colonne_gauche, colonne_droite):
        #Le point se trouve exactement sur une colonne du treillis
        if colonne_droite == colonne_gauche:
            if colonne_gauche < abs(colonne_droite - self.nombre_colonnes + 1):
                return colonne_gauche, colonne_droite + 1
            else:
                return colonne_gauche - 1, colonne_droite
        return colonne_gauche, colonne_droite

    def reglerConflitLignes(self, ligne_basse, ligne_haute):
        #Le point se trouve exactement sur une ligne du treillis
        if ligne_basse == ligne_haute:
            if ligne_basse < abs(ligne_haute - self.nombre_lignes + 1):
                return ligne_basse , ligne_haute + 1
            else:
                return ligne_basse - 1, ligne_haute 
        return ligne_basse, ligne_haute

    def avoirLigneColonnesCasesVoisines(self, position):
        ligne_basse = self.avoirLigneBasse(position)
        ligne_haute = self.avoirLigneHaute(position)
        colonne_gauche = self.avoirColonneGauche(position)
        colonne_droite = self.avoirColonneDroite(position)

        ligne_basse, ligne_haute = self.reglerConflitLignes(
            ligne_basse,
            ligne_haute)

        colonne_gauche, colonne_droite = self.reglerConflitColonnes(
            colonne_gauche,
            colonne_droite)

        return ligne_basse, ligne_haute, colonne_gauche, colonne_droite

    def avoirPositionRelative(self, point):
        ligne_basse, ligne_haute, colonne_gauche, colonne_droite = (
            self.avoirLigneColonnesCasesVoisines(point))

        origine_relative = Vec2d(
            self.avoirPositionColonne(colonne_gauche),
            self.avoirPositionLigne(ligne_basse))

        return (point - origine_relative) / self.precision

class InterpolationChampScalaire(Treillis):

    def avoirGrandientParInterpolationBilineaire(self, position):
        #On derive la formule d'interpolation bilineaire
        ligne_basse, ligne_haute, colonne_gauche, colonne_droite = (
            self.avoirLigneColonnesCasesVoisines(position))

        valeur_1_1 = self[base.Case(ligne_basse, colonne_gauche)]
        valeur_1_2 = self[base.Case(ligne_haute, colonne_gauche)]
        valeur_2_2 = self[base.Case(ligne_haute, colonne_droite)]
        valeur_2_1 = self[base.Case(ligne_basse, colonne_droite)]

        y_1 = self.avoirPositionLigne(ligne_basse)
        y_2 = self.avoirPositionLigne(ligne_haute)
        x_1 = self.avoirPositionColonne(colonne_gauche)
        x_2 = self.avoirPositionColonne(colonne_droite)

        delta_x = x_2 - x_1
        delta_y = y_2 - y_1
        dx = position.x - x_1
        dy = position.y - y_1

        delta_f_x = valeur_2_1 - valeur_1_1
        delta_f_y = valeur_1_2 - valeur_1_1
        delta_f_x_y = valeur_1_1 + valeur_2_2 - valeur_2_1 - valeur_1_2

        return Vec2d(
            delta_f_x / delta_x + delta_f_x_y * dy / (delta_x * delta_y),
            delta_f_y / delta_y + delta_f_x_y * dx / (delta_x * delta_y))

    def avoirDistanceRelativeCase(self, case_1, case_2):
        return math.sqrt(
            (case_1.ligne - case_2.ligne)** 2
            + (case_1.colonne - case_2.colonne)**2)

    def avoirTauxDeVariationRelatif(self, case_1, case_2):
        dl = self.avoirDistanceRelativeCase(case_2, case_1)
        return (self[case_1] - self[case_2]) / dl

    def avoirDeriveXCaseRelative(self, case):
        case_1 = base.Case(1, 0) + case
        case_2 = base.Case(-1, 0) + case
        return self.avoirTauxDeVariationRelatif(case_1, case_2)

    def avoirDeriveYCaseRelative(self, case):
        case_1 = base.Case(0, 1) + case
        case_2 = base.Case(0, -1) + case
        return self.avoirTauxDeVariationRelatif(case_1, case_2)

    def avoirDeriveXYCaseRelative(self, case):
        case_1 = base.Case(0, 1) + case
        case_2 = base.Case(0, -1) + case
        derive_x_1 = self.avoirDeriveXCaseRelative(case_1)
        derive_x_2 = self.avoirDeriveXCaseRelative(case_2)

        dy = self.avoirDistanceRelativeCase(case_1, case_2)
        
        return (derive_x_1 - derive_x_2) / dy

    def avoirMatriceBicubic(self, position):
        matrice_coefficients = np.matrix([
            [ 1, 0, 0, 0 ],
            [ 0, 0, 1, 0 ],
            [ -3, 3, -2, -1 ],
            [ 2, -2, 1, 1 ] ])

        ligne_basse, ligne_haute, colonne_gauche, colonne_droite = (
            self.avoirLigneColonnesCasesVoisines(position))

        haut_gauche = base.Case(ligne_haute, colonne_gauche)
        haut_droit = base.Case(ligne_haute, colonne_droite)
        bas_gauche = base.Case(ligne_basse, colonne_gauche)
        bas_droit = base.Case(ligne_basse, colonne_droite)

        template = np.matrix([
            [ bas_gauche, haut_gauche ],
            [ bas_droit, haut_droit ] ])

        block_haut_gauche = base.mapMatrix(self.__getitem__, template)
        block_haut_droit = base.mapMatrix(self.avoirDeriveYCaseRelative, template)
        block_bas_gauche = base.mapMatrix(self.avoirDeriveXCaseRelative, template)
        block_bas_droit = base.mapMatrix(self.avoirDeriveXYCaseRelative, template)

        block_gauche = np.concatenate(
            (block_haut_gauche, block_bas_gauche),
            axis=0)

        block_droit = np.concatenate(
            (block_haut_droit, block_bas_gauche),
            axis=0)

        matrice_valeurs = np.concatenate((block_gauche, block_droit), axis=1)

        return matrice_coefficients * matrice_valeurs * matrice_coefficients.T

    def avoirLigneVandermonde(self, scalaire):
        return np.matrix([ 1, scalaire, scalaire**2, scalaire**3 ])

    def avoirLigneVandermondeDerivee(self, scalaire):
        return np.matrix([ 0, 1, 2 * scalaire, 3 * scalaire**2 ])

    def avoirValeurParInterpolationBicubic(self, position):
        x, y = self.avoirPositionRelative(position)

        X = self.avoirLigneVandermonde(x)
        Y = self.avoirLigneVandermonde(y)

        matrice_bicubic = self.avoirMatriceBicubic(position)

        return X * matrice_bicubic * Y.T

    def avoirGradientParInterpolationBicubic(self, position):
        #On dérive la formule d'interpolation bicubic
        x, y = self.avoirPositionRelative(position)

        X = self.avoirLigneVandermonde(x)
        DX = self.avoirLigneVandermondeDerivee(x)
        Y = self.avoirLigneVandermonde(y)
        DY = self.avoirLigneVandermondeDerivee(y)

        matrice_bicubic = self.avoirMatriceBicubic(position)
        
        return Vec2d(DX * matrice_bicubic * Y.T, X * matrice_bicubic * DY.T)
        

    def avoirGradiantPosition(self, position):
        return self.avoirGradientParInterpolationBicubic(position)

class SpaceHash(QuadrillageEspace):
    '''Keywords argument: precision, position, hauteur, largeur, valeur_defaut (None)'''

    def avoirLignePoint(self, point):
        return math.floor((point.y - self.position.y) / self.precision)

    def avoirColonnePoint(self, point):
        return math.floor((point.x - self.position.x) / self.precision)

    def avoirCasePoint(self, point):
        return base.Case(
            self.avoirLignePoint(point),
            self.avoirColonnePoint(point))

    def avoirValeurPlusProche(self, point):
        return self[self.avoirCaseAvecCentrePlusProche(point)]

    def avoirPositionLigne(self, ligne):
        return self.position.y + (ligne + 1 / 2) * self.precision

    def avoirPositionColonne(self, colonne):
        return self.position.x + (colonne + 1 / 2) * self.precision

    def avoirCaseAvecCentrePlusProche(self, point):
        case_point = self.avoirCasePoint(point)
        cases_proches = itertools.chain(
            case_point.genererCaseAdjacentes(base.Case.genererQuatreDirections()),
            [case_point])
        cases_proches_valides = filter(
            self.__contains__,
            cases_proches)

        distance_a_point = lambda case: self.avoirCentreCase(case).get_distance(point)

        return min(cases_proches_valides, key=distance_a_point)
