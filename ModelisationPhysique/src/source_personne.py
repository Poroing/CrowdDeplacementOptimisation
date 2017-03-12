from personne import Personne

class Source(object):

    def __init__(self, espace, position, periode):
        self.periode = periode
        self.position = position
        self.espace = espace 
        self.temps_derniere_ajout = 0

    def mettreAJour(self, temps):
        personne = None
        if temps - self.temps_derniere_ajout > self.periode:
            personne = Personne(self.position, self.espace)
            self.espace.ajouterPersonne(personne)
            self.temps_derniere_ajout = temps
        return personne
