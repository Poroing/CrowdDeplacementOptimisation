import geometrie

class LieuFerme(geometrie.SimpleRectangle):

    def __init__(self,liste_portes, largeur=400, hauteur=800, position=(0, 0)):
        super().__init__(position, largeur, hauteur)
        self.liste_portes = liste_portes

    def avoirCentrePorte(self, porte):
        mur = self.avoirCote(porte['mur'])
        return mur.avoirPositionPourcentage(porte['position'])
    
    def avoirCentrePortes(self):
        sortie = []
        
        for porte in self.liste_portes :
            sortie.append(self.avoirCentrePorte(porte))
            
        return sortie

