from pymunk.vec2d import Vec2d
import pymunk

class LieuFerme(object):

    def __init__(self,liste_portes, largeur=400, hauteur=800, position=(0, 0)):
        self.largeur = largeur
        self.hauteur = hauteur
        self.position = Vec2d(position)
        self.liste_portes = liste_portes

    def avoirCentrePorte(self, porte):
        
        if porte['mur'] == "bas" :
            return self.position + Vec2d(self.largeur * porte['position'], 0)
        if porte['mur'] == "gauche" :
            return self.position + Vec2d(0, self.hauteur * porte['position'])
        if porte['mur'] == "haut" :
            return self.position + Vec2d(self.largeur * porte['position'], self.hauteur)
        if porte['mur'] == "droite" :
            return self.position + Vec2d(self.largeur, self.hauteur * porte['position'])
    
    def avoirCentrePortes(self):
        
        sortie = []
        
        for porte in self.liste_portes :
            sortie.append(self.avoirCentrePorte(porte))
            
        return sortie

    def pointEstAExterieur(self, point):
        return ( point.x > self.position.x + self.largeur or point.x < self.position.x
            or point.y > self.position.y + self.hauteur or point.y < self.position.y)


